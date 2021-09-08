import helper


class ExploreExtensiveMargin:
    def __init__(self, img_filepath):
        self.img_filepath = img_filepath
        self.jobs = None

    def run(self):
        self.jobs = helper.get_all_postings()
        self.jobs.dropna(subset=['AES'], inplace=True)

        sector_job_count = self.count_jobs_by_sector()
        self.prop_jobs_by_sector(sector_job_count)

    def count_jobs_by_sector(self):
        df = self.jobs.groupby(['AES', 'year'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')
        df.rename(columns={'scaled_JOB_POST_ID': 'overall_job_count'}, inplace=True)
        df.drop(columns=['JOB_POST_ID'], inplace=True)
        return df

    def prop_jobs_by_sector(self, sector_job_count):
        year_df = self.jobs.groupby(['year'])['JOB_POST_ID'].count().reset_index()
        year_df = helper.scale_counts(year_df, 'JOB_POST_ID')
        year_df.rename(columns={'scaled_JOB_POST_ID': 'yearly_overall_job_count'}, inplace=True)
        year_df.drop(columns=['JOB_POST_ID'], inplace=True)

        df = sector_job_count.merge(year_df, on=['year'], how='left')
        df['overall_job_prop'] = df['overall_job_count'] / df['yearly_overall_job_count']
        helper.save_csv(df, 'data/analysis/jobs_by_sector.csv')
