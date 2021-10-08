import os
import pandas as pd
import config
from datetime import datetime


class ProcessMCFJobs:
    def __init__(self, postings_dir, output_filepath, ssoc2015_to_2020_filepath):
        self.postings_dir = postings_dir
        self.output_filepath = output_filepath

        self.ssoc_mapping = pd.read_excel(ssoc2015_to_2020_filepath, skiprows=4)

    def run(self):
        self.job_to_ssoc(self.postings_dir)

    def job_to_ssoc(self, folder):
        # Combine job info and detail files
        jobdetail_filepaths = [folder + x for x in os.listdir(folder) if x.startswith('JOB_POST_DETAIL')]
        jobinfo_filepaths = [config.jobposting_detail_info_mapping[x] for x in jobdetail_filepaths]

        for idx, path in enumerate(jobdetail_filepaths):
            print(path)
            detail = pd.read_csv(path, delimiter='\t', encoding="ISO-8859-1", error_bad_lines=False)
            info = pd.read_csv(jobinfo_filepaths[idx], delimiter='\t', encoding="ISO-8859-1", error_bad_lines=False)

            # check column title (2020-07 and 08 data is a bit noisy)
            bool = [True if (x.startswith('^') and x.endswith('^')) else False for x in detail.columns]
            if sum(bool) == len(bool):
                detail = detail.applymap(lambda x: str(x)[1:-1])
                detail.columns = [str(x)[1:-1] for x in detail.columns]

            # Get AES sector
            info[['HIRE_ORG_SSIC_CODE', 'JOB_SSOC_CODE_6D']] = info[['HIRE_ORG_SSIC_CODE', 'JOB_SSOC_CODE_6D']].astype(
                str)
            info['AES'] = info['HIRE_ORG_SSIC_CODE'].apply(lambda x: self.ssic_to_aes(x))

            # Get SSOC2020 code of job (from SSOC2015)
            self.ssoc_mapping[['SSOC 2020', 'SSOC 2015 (Version 2018)']] = self.ssoc_mapping[
                ['SSOC 2020', 'SSOC 2015 (Version 2018)']].astype(str)
            ssoc_mapping = self.ssoc_mapping[['SSOC 2020', 'SSOC 2015 (Version 2018)']]
            info = info.merge(ssoc_mapping, left_on=['JOB_SSOC_CODE_6D'], right_on=['SSOC 2015 (Version 2018)'],
                              how='left')

            # Drop jobs that don't have SSOC2020 code
            info.dropna(subset=['SSOC 2020'], inplace=True)

            # Get SSOC4D and SSOC1D
            info['SSOC4D'] = info['SSOC 2020'].apply(lambda x: x[:4])
            info['SSOC1D'] = info['SSOC 2020'].apply(lambda x: x[:1])

            # Merge job info (SSOC2020 etc.) with job details (job description etc.)
            merged = detail.merge(info[['JOB_POST_ID', 'SSOC4D', 'SSOC1D', 'HIRE_ORG_SSIC_CODE', 'AES']],
                                  on='JOB_POST_ID', how='inner')

            # Drop jobs that are non-PMET (Drop SSOC1D 4-9)
            pmet = ['1', '2', '3']
            merged_filtered = merged[merged['SSOC1D'].isin(pmet)]
            print(len(merged) - len(merged_filtered), 'non-PMET jobs dropped')

            merged_filtered['date'] = merged_filtered['YYYYMM'].apply(lambda x: datetime.strptime(str(x), '%Y%m'))
            merged_filtered['year'] = merged_filtered['date'].apply(lambda x: x.year)
            merged_filtered['month'] = merged_filtered['date'].apply(lambda x: x.month)

            # clean file
            merged_filtered.drop_duplicates(inplace=True)
            merged_filtered.dropna(subset=['JOB_POST_DESC'], inplace=True)
            merged_filtered=merged_filtered[merged_filtered['JOB_POST_DESC']!='']

            output = self.output_filepath.format(path.split('/')[-1].split('.')[0])
            merged_filtered.to_csv(output, index=False)

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
