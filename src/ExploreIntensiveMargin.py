import helper
import matplotlib.pyplot as plt
import seaborn as sns
import os


class ExploreIntensiveMargin:
    def __init__(self, img_filepath, analysis_filepath):
        self.img_filepath = img_filepath
        self.analysis_filepath = analysis_filepath

        self.jobs = None

    def run(self):
        self.jobs = helper.get_all_postings()
        self.filter_ssoc()

        count_jobs_by_ssoc = self.count_jobs_by_ssoc()
        avg_subtracks_by_ssoc = self.avg_subtracks_per_job_in_ssoc(count_jobs_by_ssoc)
        self.change_avg_subtracks_per_job_in_ssoc(avg_subtracks_by_ssoc)

        self.subtracks_pdf()
        self.subtracks_cdf()

    def filter_ssoc(self):
        # Filter to include SSOCs that have increase in % or high absolute % in Finance & Insurance, Business Services, and Information & Communication
        ssocs = [2122, 2123, 2152, 2511, 2512, 2521, 2524]
        self.jobs = self.jobs[self.jobs['SSOC4D'].isin(ssocs)]

    def count_jobs_by_ssoc(self):
        # count the total number of jobs per ssoc per year
        df = self.jobs.groupby(['SSOC4D', 'year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'total_jobs'}, inplace=True)

        return df

    def avg_subtracks_per_job_in_ssoc(self, count_jobs_by_ssoc):
        # For each SSOC, get the average number of subtracks per job posting per year
        df = self.jobs.groupby(['SSOC4D', 'year'])['num_subtracks_final'].mean().reset_index()
        df.rename(columns={'num_subtracks_final': 'avg_num_subtracks_per_job_posting'}, inplace=True)

        # get total number of jobs
        df = df.merge(count_jobs_by_ssoc, on=['SSOC4D', 'year'])

        filepath = self.analysis_filepath.format('avg_subtracks_by_ssoc')
        helper.save_csv(df, filepath)
        return df

    def change_avg_subtracks_per_job_in_ssoc(self, avg_subtracks_by_ssoc):
        # get 2021-2018 change in avg subtracks per job per SSOC
        df = avg_subtracks_by_ssoc[avg_subtracks_by_ssoc['year'].isin(['2018', '2021'])]
        df.sort_values(by=['SSOC4D', 'year'], ascending=True, inplace=True)
        df['2021-2018_diff'] = df['avg_num_subtracks_per_job_posting'].diff()
        df = df[df['year'] == '2021']

        filepath = self.analysis_filepath.format('avg_subtracks_change_by_ssoc')
        helper.save_csv(df, filepath)

    def subtracks_pdf(self):
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
        df = self.jobs[self.jobs['num_subtracks_final'] != 0]
        df.sort_values(by=['year'], inplace=True)

        for year in df['year'].unique():
            temp = df[df['year'] == year]
            sns.kdeplot(temp['num_subtracks_final'].tolist(), label=year, alpha=0.8)

        # Add labels
        plt.title('PDF of Subtracks per Job Posting')
        plt.xlabel('Number of subtracks required per job posting')
        plt.ylabel('Proportion of job postings')
        plt.legend(title='Year')

        filename = self.img_filepath.format('subtracks_pdf')
        plt.savefig(filename, transparent=True)
        plt.close()

    def subtracks_cdf(self):
        df = self.jobs[self.jobs['num_subtracks_final'] != 0]
        df.sort_values(by=['year'], inplace=True)

        for year in df['year'].unique():
            temp = df[df['year'] == year]
            sns.kdeplot(temp['num_subtracks_final'].tolist(), cumulative=True, label=year, alpha=0.8)

        # Add labels
        plt.title('CDF of Subtracks per Job Posting')
        plt.xlabel('Number of subtracks required per job posting')
        plt.ylabel('Proportion of job postings')
        plt.legend(title='Year')

        filename = self.img_filepath.format('subtracks_cdf')
        plt.savefig(filename, transparent=True)
        plt.close()
