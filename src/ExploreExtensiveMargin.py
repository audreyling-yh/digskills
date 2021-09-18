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
        self.prop_ict_jobs_by_sector(sector_job_count, sector_ict_job_count)

        ssoc_ict_job_count = self.count_ict_ssoc_by_sector()
        self.prop_ict_ssoc_by_sector(sector_ict_job_count, ssoc_ict_job_count)

    def indicate_ict_job(self):
        # get ICT SSOC4Ds
        ict_jobs = pd.read_csv(self.ict_jobs_filepath)
        ict_ssoc = ict_jobs['SSOC4DMapping'].unique().tolist()

        # true if the job's SSOC4D is an ICT SSOC4D
        self.jobs['ict'] = self.jobs['SSOC4D'].isin(ict_ssoc)

    def count_jobs_by_year(self):
        # count the total number of jobs each year
        df = self.jobs.groupby(['year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'yearly_overall_job_count'}, inplace=True)
        return df

    def count_jobs_by_sector(self):
        # count the total number of jobs in each sector each year
        df = self.jobs.groupby(['AES', 'year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'sector_overall_job_count'}, inplace=True)
        return df

    def count_ict_jobs_by_sector(self):
        # count the total number of ICT/non-ICT jobs in each sector each year
        df = self.jobs.groupby(['AES', 'year', 'ict'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'job_count'}, inplace=True)
        return df

    def count_ict_jobs_by_year(self):
        # count the total number of ICT/non-ICT jobs each year
        df = self.jobs.groupby(['year', 'ict'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'job_count'}, inplace=True)
        return df

    def prop_jobs_by_sector(self, year_job_count, sector_job_count):
        # get the proportion of all jobs in each sector each year
        df = sector_job_count.merge(year_job_count, on=['year'], how='left')
        df['total jobs in sector/total jobs across all sectors'] = df['sector_overall_job_count'] / df[
            'yearly_overall_job_count']
        filepath = self.analysis_filepath.format('overall_jobs_by_sector')
        helper.save_csv(df, filepath)

    def prop_ict_jobs_by_year(self, year_job_count, year_ict_job_count):
        # get the proportion of ICT/non-ICT jobs each year
        df = year_ict_job_count.merge(year_job_count, on=['year'], how='left')
        df['total ict jobs/total jobs'] = df['job_count'] / df['yearly_overall_job_count']
        filepath = self.analysis_filepath.format('ict_jobs_by_year')
        helper.save_csv(df, filepath)

    def prop_ict_jobs_by_sector(self, sector_job_count, sector_ict_job_count):
        # get the proportion of ICT/non-ICT jobs in each sector each year
        df = sector_ict_job_count.merge(sector_job_count, on=['year', 'AES'], how='left')
        df['total ict jobs in sector/total jobs in sector'] = df['job_count'] / df['sector_overall_job_count']
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

    def count_ict_ssoc_by_sector(self):
        # count the total number of jobs in each ICT SSOC4D in each sector each year
        df = self.jobs[self.jobs['ict']]
        df = df.groupby(['year', 'AES', 'SSOC4D'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'job_count'}, inplace=True)
        return df

    def prop_ict_ssoc_by_sector(self, sector_ict_job_count, ssoc_ict_job_count):
        sector_ict_job_count.rename(columns={'job_count': 'sector_ict_job_count'}, inplace=True)
        sector_ict_job_count = sector_ict_job_count[sector_ict_job_count['ict']]
        sector_ict_job_count.drop(columns=['ict'], inplace=True)

        # get the proportion of jobs in each ICT SSOC4D in each sector each year
        df = ssoc_ict_job_count.merge(sector_ict_job_count, on=['year', 'AES'], how='left')
        df['total jobs in ssoc in sector/total ict jobs in sector'] = df['job_count'] / df['sector_ict_job_count']
        filepath = self.analysis_filepath.format('ict_jobs_by_ssoc')
        helper.save_csv(df, filepath)
        return df
