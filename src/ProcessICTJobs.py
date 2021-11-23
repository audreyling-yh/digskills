import pandas as pd


class ProcessICTJobs:
    def __init__(self, ssg_jobs_filepath, ssoc_index_filepath, output_filepath):
        self.ssg_jobs_filepath = ssg_jobs_filepath
        self.ssoc_index_filepath = ssoc_index_filepath
        self.output_filepath = output_filepath

        self.ssg_jobs = pd.DataFrame()
        self.ssoc_index = pd.DataFrame()
        self.df = pd.DataFrame()

    def run(self):
        self.read_data()
        self.clean_ssoc_index()
        self.clean_ssg_jobs()

        self.get_ict_jobs()
        self.map_role_to_ssoc()
        self.df.to_csv(self.output_filepath, index=False)

    def read_data(self):
        # read ssg skills framework job roles
        self.ssg_jobs = pd.read_csv(self.ssg_jobs_filepath)

        # read ssoc-job role index
        self.ssoc_index = pd.read_excel(self.ssoc_index_filepath, skiprows=7)

    def clean_ssoc_index(self):
        # filter to Skills Framework job roles
        self.ssoc_index = self.ssoc_index[self.ssoc_index["Singapore Skills Framework's Job Roles*"] == 'x']

        # lowercase job roles
        self.ssoc_index['job_role'] = self.ssoc_index['SSOC 2020 Alphabetical Index Description'].apply(
            lambda x: x.lower())

        # remove anything in brackets
        self.ssoc_index['job_role'] = self.ssoc_index['job_role'].apply(lambda x: x.split('(')[0].strip())

    def clean_ssg_jobs(self):
        # text cleaning
        self.ssg_jobs['job_role'] = self.ssg_jobs['job_role'].apply(
            lambda x: '/'.join([i.strip() for i in x.split('/')]))

    def get_ict_jobs(self):
        # Filter all SSG jobs to only ICT ones
        self.ssg_jobs = self.ssg_jobs[self.ssg_jobs['sector'] == 'infocomm technology']

        # Filter out sales track
        self.ssg_jobs = self.ssg_jobs[self.ssg_jobs['track'] != 'sales and marketing']

    def map_role_to_ssoc(self):
        # merge dfs
        self.df = self.ssg_jobs.merge(self.ssoc_index[['job_role', 'SSOC 2020']], on='job_role', how='left')

        # Drop not-purely-ICT SSOC4Ds
        self.df['ssoc4d'] = self.df['SSOC 2020'].apply(lambda x: x[:4])
        excluded_ssocs = ['1221',  # Sales and business dev managers
                          '2411',  # accountants
                          '2433',  # specialised goods sales professionals
                          '1323',  # construction managers
                          '2431'  # advertising and markerting professionals
                          ]
        self.df = self.df[~self.df['ssoc4d'].isin(excluded_ssocs)]

        # clean df
        self.df.drop(columns=['ssoc4d', 'tsc_id', 'tsc_category', 'tsc_title', 'proficiency_level'], inplace=True)
        self.df.drop_duplicates(inplace=True)
