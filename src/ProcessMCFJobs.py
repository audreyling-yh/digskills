import os
import pandas as pd
import config
import helper
from datetime import datetime


class ProcessMCFJobs:
    def __init__(self, postings_dir, output_filepath, ssoc2015_to_2020_filepath):
        self.postings_dir = postings_dir
        self.output_filepath = output_filepath
        self.ssoc2015_to_2020_filepath = ssoc2015_to_2020_filepath

        self.ssoc_mapping = pd.DataFrame()

    def run(self):
        self.read_data()
        self.job_to_ssoc(self.postings_dir)

    def read_data(self):
        # get mapping from ssoc 2015 to ssoc 2020
        self.ssoc_mapping = pd.read_excel(self.ssoc2015_to_2020_filepath, skiprows=4)

        cols = ['SSOC 2020', 'SSOC 2015 (Version 2018)']
        self.ssoc_mapping[cols] = self.ssoc_mapping[cols].astype(str)
        self.ssoc_mapping = self.ssoc_mapping[cols]

    def job_to_ssoc(self, folder):
        # Combine job info and detail files
        jobdetail_filepaths = [folder + x for x in os.listdir(folder) if x.startswith('JOB_POST_DETAIL')]
        jobinfo_filepaths = [config.jobposting_detail_info_mapping[x] for x in jobdetail_filepaths]

        for idx, path in enumerate(jobdetail_filepaths):
            print(path)
            detail = pd.read_csv(path, delimiter='\t', encoding="ISO-8859-1", error_bad_lines=False)
            info = pd.read_csv(jobinfo_filepaths[idx], delimiter='\t', encoding="ISO-8859-1", error_bad_lines=False)

            # prep data
            detail = self.clean_noise(detail)
            info = self.prep_data(info)

            # Get AES sector and ssoc info
            info['AES'] = info['HIRE_ORG_SSIC_CODE'].apply(lambda x: self.ssic_to_aes(x))
            info = self.ssoc2015_to_ssoc2020(info)
            info = self.get_ssoc4d_and_1d(info)

            # Merge job info (SSOC2020 etc.) with job details (job description etc.)
            merged = detail.merge(info[['JOB_POST_ID', 'SSOC 2020', 'SSOC4D', 'SSOC1D', 'HIRE_ORG_SSIC_CODE', 'AES']],
                                  on='JOB_POST_ID', how='inner')

            # drop non-pmet jobs
            merged = self.drop_non_pmet(merged)

            df = self.clean_final_df(merged)

            # get programming languages
            df['programming_languages'] = helper.extract_programming_languages(df['JOB_POST_DESC'])

            output = self.output_filepath.format(path.split('/')[-1].split('.')[0])
            df.to_csv(output, index=False)

    def prep_data(self, info_df):
        info_df[['HIRE_ORG_SSIC_CODE', 'JOB_SSOC_CODE_6D']] = info_df[
            ['HIRE_ORG_SSIC_CODE', 'JOB_SSOC_CODE_6D']].astype(str)

        return info_df

    def clean_noise(self, detail_df):
        # check column title (2020-07 and 08 data is a bit noisy)
        bool = [True if (x.startswith('^') and x.endswith('^')) else False for x in detail_df.columns]
        if sum(bool) == len(bool):
            detail_df = detail_df.applymap(lambda x: str(x)[1:-1])
            detail_df.columns = [str(x)[1:-1] for x in detail_df.columns]

        return detail_df

    def ssic_to_aes(self, ssic):
        # Get AES sector of employer
        aes_mapping = config.aes_ssic_mapping
        aes = None

        for k, v in aes_mapping.items():
            range_start = k.split(',')[0]
            range_end = k.split(',')[1]

            if range_start <= ssic[:2] <= range_end:
                aes = v

        return aes

    def ssoc2015_to_ssoc2020(self, info_df):
        # Get SSOC2020 code of job (from SSOC2015)
        info_df = info_df.merge(self.ssoc_mapping, left_on=['JOB_SSOC_CODE_6D'], right_on=['SSOC 2015 (Version 2018)'],
                                how='left')

        # Drop jobs that don't have SSOC2020 code
        info_df.dropna(subset=['SSOC 2020'], inplace=True)

        return info_df

    def get_ssoc4d_and_1d(self, info_df):
        # Get SSOC4D and SSOC1D
        info_df['SSOC4D'] = info_df['SSOC 2020'].apply(lambda x: x[:4])
        info_df['SSOC1D'] = info_df['SSOC 2020'].apply(lambda x: x[:1])

        return info_df

    def drop_non_pmet(self, df):
        # Drop jobs that are non-PMET (Drop SSOC1D 4-9)
        pmet = ['1', '2', '3']
        df_filtered = df[df['SSOC1D'].isin(pmet)]
        print(len(df) - len(df_filtered), 'non-PMET jobs dropped')

        return df_filtered

    def clean_final_df(self, df):
        # create new date columns
        df['date'] = df['YYYYMM'].apply(lambda x: datetime.strptime(str(x), '%Y%m'))
        df['year'] = df['date'].apply(lambda x: x.year)
        df['month'] = df['date'].apply(lambda x: x.month)

        # clean file
        df.dropna(subset=['JOB_POST_DESC'], inplace=True)
        df.drop_duplicates(subset=['JOB_POST_DESC'], keep='last', inplace=True)
        df = df[df['JOB_POST_DESC'] != '']

        return df
