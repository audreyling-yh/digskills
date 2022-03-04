import os
import ast
import vaex
import config
import pandas as pd
from datetime import datetime
from flashtext import KeywordProcessor


class ProcessMCFJobs:
    def __init__(self, mcf_raw_folder, mcf_raw_filepath, mcf_processed_folder, mcf_processed_filepath,
                 ssocmapping_filepath, appstools_filepath, ict_roles_filepath, overwrite=False):
        self.mcf_raw_folder = mcf_raw_folder
        self.mcf_raw_filepath = mcf_raw_filepath
        self.mcf_processed_folder = mcf_processed_folder
        self.mcf_processed_filepath = mcf_processed_filepath
        self.ssocmapping_filepath = ssocmapping_filepath
        self.appstools_filepath = appstools_filepath
        self.ict_roles_filepath = ict_roles_filepath
        self.overwrite = overwrite

        self.kwproc = None
        self.ict_ssoc = []

    def run(self):
        self.init_keyword_processer()
        self.get_ict_ssoc()

        folders = [x for x in os.listdir(self.mcf_raw_folder) if os.path.isdir(self.mcf_raw_folder + x)]

        # if true, overwrite all existing processed files; re-process
        if not self.overwrite:
            print('NOT overwriting existing processed files')
            existing_files = [x.split('.')[0] for x in os.listdir(self.mcf_processed_folder)]
            folders = [x for x in folders if x not in existing_files]

        # loop for each month
        for i in folders:
            print('Processing raw {} job postings'.format(i))
            folderpath = self.mcf_raw_folder + i

            # get job postings for the month
            df = self.compile_jobpostings(i, folderpath)

            # convert SSIC to AES sector
            df = self.ssic_to_aes(df)

            # convert SSOC 2010 to SSOC 2020
            df = self.ssoc2010_to_ssoc2020(df)

            # drop non-PMET jobs
            df = self.drop_non_pmet(df)

            # get year and month cols
            df = self.get_date_cols(df)

            # cleaning
            df = self.clean_df(df)

            # extract apps and tools
            df = self.extract_appstools(df)

            # indicate if ict role
            df = self.indicate_ict(df)

            # manage object col types
            df = self.manage_dtypes(df)

            # save as hdf5
            df = vaex.from_pandas(df)
            df.export(self.mcf_processed_filepath.format(i))

    def init_keyword_processer(self):
        # read apps and tools
        appstools = pd.read_excel(self.appstools_filepath)
        appstools['skill_leaf'] = appstools['skill_leaf'].apply(list)
        appstools = dict(zip(appstools['skill'], appstools['skill_leaf']))

        # add keywords
        self.kwproc = KeywordProcessor()
        self.kwproc.add_keywords_from_dict(appstools)
        self.kwproc.add_keywords_from_list(list(appstools.keys()))

    def get_ict_ssoc(self):
        # read ict roles
        roles = pd.read_csv(self.ict_roles_filepath)
        roles['SSOC 2020'] = roles['SSOC 2020'].apply(ast.literal_eval)
        roles = roles.explode('SSOC 2020')
        self.ict_ssoc = [x for x in roles['SSOC 2020'].unique() if x != '0']

    def compile_jobpostings(self, foldername, folderpath):
        print('\tCompiling job postings')

        # convert the job info and detail text files into dfs
        job_info_files = [self.mcf_raw_filepath.format(foldername, x) for x in os.listdir(folderpath) if
                          x.startswith('JOB_POST') and 'DETAILS' not in x]
        job_detail_files = [self.mcf_raw_filepath.format(foldername, x) for x in os.listdir(folderpath) if
                            x.startswith('JOB_POST_DETAILS')]

        info_df = self.txt_to_df(job_info_files)
        detail_df = self.txt_to_df(job_detail_files)

        # column cleaning
        detail_df = self.clean_noise(detail_df)

        # merge the dfs
        df = info_df.merge(detail_df, on=['YYYYMM', 'JOB_POST_ID'], how='inner')

        return df

    def txt_to_df(self, filepaths):
        print('\tConverting {} to dataframe'.format(filepaths))

        # convert txt files to df and combine if more than 2 txt JOB_POST or DETAILS file per folder
        df = pd.DataFrame()
        for i in filepaths:

            # set delimiter
            with open(i) as f:
                first_line = f.readline()
                delimiter = '|' if '|' in first_line else '\t'

            temp = pd.read_csv(i, delimiter=delimiter, encoding="ISO-8859-1", error_bad_lines=False,
                               warn_bad_lines=True, dtype={'YYYYMM': 'str', 'JOB_POST_ID': 'str'})
            df = pd.concat([df, temp])

        df.drop_duplicates(inplace=True)

        return df

    def clean_noise(self, detail_df):
        # check column title (2020-07 and 08 data is a bit noisy)
        bool = [True if (x.startswith('^') and x.endswith('^')) else False for x in detail_df.columns]
        if sum(bool) == len(bool):
            detail_df = detail_df.applymap(lambda x: str(x)[1:-1])
            detail_df.columns = [str(x)[1:-1] for x in detail_df.columns]

        return detail_df

    def ssic_to_aes(self, df):
        print('\tConverting SSIC to AES sectors')

        # convert SSIC to AES sectors
        df['HIRE_ORG_SSIC_CODE'] = df['HIRE_ORG_SSIC_CODE'].astype(str)
        df['AES'] = df['HIRE_ORG_SSIC_CODE'].apply(self.get_aes_from_ssic)

        return df

    def get_aes_from_ssic(self, ssic):
        # Get AES sector from an SSIC code
        aes_mapping = config.aes_ssic_mapping
        aes = None

        for k, v in aes_mapping.items():
            range_start = k.split(',')[0]
            range_end = k.split(',')[1]

            if range_start <= ssic[:2] <= range_end:
                aes = v

        return aes

    def ssoc2010_to_ssoc2020(self, df):
        print('\tConverting SSOC 2010 to SSOC 2020')

        # read ssoc mapping
        mapping = pd.read_csv(self.ssocmapping_filepath)[['SSOC 2010', 'SSOC 2020']]

        # Get SSOC 2020 code of job (from SSOC2010)
        df['JOB_SSOC_CODE_6D'] = df['JOB_SSOC_CODE_6D'].astype(str)
        df = df.merge(mapping, left_on=['JOB_SSOC_CODE_6D'], right_on=['SSOC 2010'], how='inner')

        # Drop jobs that don't have SSOC2020 code
        df.dropna(subset=['SSOC 2020'], inplace=True)

        return df

    def drop_non_pmet(self, df):
        # Drop jobs that are non-PMET (Drop SSOC1D 4-9)
        df_filtered = df[(df['SSOC 2020'].str.startswith('1')) |
                         (df['SSOC 2020'].str.startswith('2')) |
                         (df['SSOC 2020'].str.startswith('3'))]
        print('\t{} non-PMET jobs dropped'.format(len(df) - len(df_filtered)))

        return df_filtered

    def get_date_cols(self, df):
        # create new date columns
        df['YYYYMM'] = df['YYYYMM'].apply(lambda x: datetime.strptime(str(x), '%Y%m'))
        df['year'] = df['YYYYMM'].apply(lambda x: x.year)
        df['month'] = df['YYYYMM'].apply(lambda x: x.month)

        return df

    def clean_df(self, df):
        # clean df
        df.dropna(subset=['JOB_POST_DESC'], inplace=True)
        df = df[df['JOB_POST_DESC'] != '']
        df.drop_duplicates(subset=['JOB_POST_ID'], keep='last', inplace=True)

        # sort
        df.sort_values(by=['YYYYMM', 'JOB_POST_ID'], ascending=True, inplace=True)

        return df

    def extract_appstools(self, df):
        print('\tExtracting apps and tools')

        # extract apps and tools mentioned by job description
        df['apps_tools'] = df['JOB_POST_DESC'].apply(lambda x: ';'.join(self.kwproc.extract_keywords(x)))

        return df

    def indicate_ict(self, df):
        print('\tIndicating ICT roles')

        # indicate if a job postings is an ICT job based on SSOC
        df['ict_role'] = df['SSOC 2020'].apply(lambda x: 1 if x in self.ict_ssoc else 0)

        return df

    def manage_dtypes(self, df):
        # convert object dtype cols
        df = df.convert_dtypes()
        coltypes = df.dtypes.to_dict()
        for k, v in coltypes.items():
            if v == 'object':
                try:
                    df = df.astype({k: 'float32'})
                except:
                    df = df.astype({k: 'string'})

        return df