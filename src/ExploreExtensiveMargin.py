import helper
import pandas as pd


class ExploreExtensiveMargin:
    def __init__(self, img_filepath, analysis_filepath, ict_jobs_filepath):
        self.img_filepath = img_filepath
        self.analysis_filepath = analysis_filepath
        self.ict_jobs_filepath = ict_jobs_filepath

        self.jobs = None

    def run(self):
        self.jobs = helper.get_all_postings()
        self.jobs.dropna(subset=['AES'], inplace=True)
        self.indicate_ict_job()

        year_job_count = self.count_jobs_by_year()

        sector_job_count = self.count_jobs_by_sector()
        self.prop_jobs_by_sector(year_job_count, sector_job_count)

        year_ict_job_count = self.count_ict_jobs_by_year()
        self.prop_ict_jobs_by_year(year_job_count, year_ict_job_count)

        sector_ict_job_count = self.count_ict_jobs_by_sector()
        self.prop_ict_jobs_by_sector(year_job_count, sector_ict_job_count)

        self.filter_sectors()
        ssoc_ict_job_count = self.count_ict_jobs_by_ssoc()
        ssoc_ict_job_prop=self.prop_ict_jobs_by_ssoc(year_job_count, ssoc_ict_job_count)
        self.get_change_in_prop(ssoc_ict_job_prop)

    def indicate_ict_job(self):
        # get ICT SSOC4Ds
        ict_jobs = pd.read_csv(self.ict_jobs_filepath)
        ict_ssoc = ict_jobs['SSOC4DMapping'].unique().tolist()

        # true if the job's SSOC4D is an ICT SSOC4D
        self.jobs['ict'] = self.jobs['SSOC4D'].isin(ict_ssoc)

    def count_jobs_by_year(self):
        # count the total number of jobs each year
        df = self.jobs.groupby(['year'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')
        df.rename(columns={'scaled_JOB_POST_ID': 'yearly_overall_job_count'}, inplace=True)
        df.drop(columns=['JOB_POST_ID'], inplace=True)
        return df

    def count_jobs_by_sector(self):
        # count the total number of jobs in each sector each year
        df = self.jobs.groupby(['AES', 'year'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')
        df.rename(columns={'scaled_JOB_POST_ID': 'overall_job_count'}, inplace=True)
        df.drop(columns=['JOB_POST_ID'], inplace=True)
        return df

    def count_ict_jobs_by_sector(self):
        # count the total number of ICT/non-ICT jobs in each sector each year
        df = self.jobs.groupby(['AES', 'year', 'ict'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')
        df.rename(columns={'scaled_JOB_POST_ID': 'job_count'}, inplace=True)
        df.drop(columns=['JOB_POST_ID'], inplace=True)
        return df

    def count_ict_jobs_by_year(self):
        # count the total number of ICT/non-ICT jobs each year
        df = self.jobs.groupby(['year', 'ict'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')
        df.rename(columns={'scaled_JOB_POST_ID': 'job_count'}, inplace=True)
        df.drop(columns=['JOB_POST_ID'], inplace=True)
        return df

    def prop_jobs_by_sector(self, year_job_count, sector_job_count):
        # get the proportion of all jobs in each sector each year
        df = sector_job_count.merge(year_job_count, on=['year'], how='left')
        df['job_prop'] = df['overall_job_count'] / df['yearly_overall_job_count']
        filepath = self.analysis_filepath.format('overall_jobs_by_sector')
        helper.save_csv(df, filepath)

    def prop_ict_jobs_by_year(self, year_job_count, year_ict_job_count):
        # get the proportion of ICT/non-ICT jobs each year
        df = year_ict_job_count.merge(year_job_count, on=['year'], how='left')
        df['job_prop'] = df['job_count'] / df['yearly_overall_job_count']
        filepath = self.analysis_filepath.format('ict_jobs_by_year')
        helper.save_csv(df, filepath)

    def prop_ict_jobs_by_sector(self, year_job_count, sector_ict_job_count):
        # get the proportion of ICT/non-ICT jobs in each sector each year
        df = sector_ict_job_count.merge(year_job_count, on=['year'], how='left')
        df['job_prop'] = df['job_count'] / df['yearly_overall_job_count']
        filepath = self.analysis_filepath.format('ict_jobs_by_sector')
        helper.save_csv(df, filepath)

    def filter_sectors(self):
        # narrow down to sectors with highest proportion of ICT jobs
        sectors = ['Business Services',
                   'Information & Communications',
                   'Finance & Insurance',
                   'Wholesale & Retail Trade',
                   'Manufacturing']
        self.jobs = self.jobs[self.jobs['AES'].isin(sectors)]

    def count_ict_jobs_by_ssoc(self):
        # count the total number of ICT/non-ICT jobs in each SSOC4D each year
        df = self.jobs.groupby(['year', 'SSOC4D', 'ict'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')
        df.rename(columns={'scaled_JOB_POST_ID': 'job_count'}, inplace=True)
        df.drop(columns=['JOB_POST_ID'], inplace=True)
        return df

    def prop_ict_jobs_by_ssoc(self, year_job_count, ssoc_ict_job_count):
        # get the proportion of ICT/non-ICT jobs in each SSOC4D each year
        df = ssoc_ict_job_count.merge(year_job_count, on=['year'], how='left')
        df['job_prop'] = df['job_count'] / df['yearly_overall_job_count']
        filepath = self.analysis_filepath.format('ict_jobs_by_ssoc')
        helper.save_csv(df, filepath)
        return df

    def get_change_in_prop(self, ssc_ict_job_prop):
        # narrow down to ICT jobs
        ssc_ict_job_prop=ssc_ict_job_prop[ssc_ict_job_prop['ict']]

        # drop SSOC4Ds that don't have values for all 4 years
        temp=ssc_ict_job_prop.groupby(['SSOC4D'])['year'].nunique().reset_index()
        temp=temp[temp['year']==4]
        ssoclist=temp['SSOC4D'].tolist()
        df=ssc_ict_job_prop[ssc_ict_job_prop['SSOC4D'].isin(ssoclist)]

        # get change in proportion between 2018 and 2021
        df=df[df['year'].isin(['2018','2021'])]
        df.sort_values(by=['SSOC4D','year'],ascending=True,inplace=True)
        df['prop_diff_2018_2021']=df['job_prop'].diff()
        df = df[df['year'].isin(['2021'])]

        # clean
        df.sort_values(by=['prop_diff_2018_2021'],ascending=False,inplace=True)
        df=df[['SSOC4D','prop_diff_2018_2021']]

        filepath = self.analysis_filepath.format('ict_jobs_increase_by_ssoc')
        helper.save_csv(df, filepath)

