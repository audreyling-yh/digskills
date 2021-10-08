import os
import ast
import pandas as pd
import numpy as np
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
from wordcloud import WordCloud, STOPWORDS


class AnalyseIntensiveMargin:
    def __init__(self, img_filepath, analysis_filepath, ict_jobs_filepath):
        self.img_filepath = img_filepath
        self.analysis_filepath = analysis_filepath
        self.ict_jobs_filepath = ict_jobs_filepath

        self.ict_ssoc = None
        self.jobs = None

    def run(self):
        self.jobs = helper.get_all_postings()
        self.jobs = self.indicate_ict_job(self.jobs)

        # count_jobs_by_ssoc = self.count_jobs_by_ssoc()
        # avg_tsc_categories_by_ssoc = self.avg_categories_per_job_in_ssoc(count_jobs_by_ssoc)
        # self.change_avg_categories_per_job_in_ssoc(avg_tsc_categories_by_ssoc)
        #
        # self.tsc_categories_pdf()
        # self.tsc_categories_cdf()

        prop_jobs_by_tsc_category = self.prop_jobs_per_tsc_category_in_ssoc()
        self.change_prop_jobs_per_tsc_category_in_ssoc(prop_jobs_by_tsc_category)

        self.skill_word_clouds()

    def indicate_ict_job(self, df):
        # get ICT SSOC4Ds
        ict_jobs = pd.read_csv(self.ict_jobs_filepath)
        self.ict_ssoc = ict_jobs['SSOC4DMapping'].unique().tolist()

        # true if the job's SSOC4D is an ICT SSOC4D
        df['ict'] = df['SSOC4D'].isin(self.ict_ssoc)

        return df

    def count_jobs_by_ssoc(self):
        # count the total number of jobs per ssoc per year
        df = self.jobs.groupby(['SSOC4D', 'ict', 'year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'total_jobs'}, inplace=True)

        return df

    def avg_categories_per_job_in_ssoc(self, count_jobs_by_ssoc):
        # For each SSOC, get the average number of tsc categories per job posting per year
        df = self.jobs.groupby(['SSOC4D', 'ict', 'year'])['tsc_category_count'].mean().reset_index()
        df.rename(columns={'tsc_category_count': 'avg_tsc_category_count_per_job'}, inplace=True)

        # get total number of jobs
        df = df.merge(count_jobs_by_ssoc, on=['SSOC4D', 'ict', 'year'])

        filepath = self.analysis_filepath.format('avg_tsc_categories_by_ssoc')
        helper.save_csv(df, filepath)
        return df

    def change_avg_categories_per_job_in_ssoc(self, avg_categories_by_ssoc):
        # get 2021-2018 change in avg tsc categories per job per SSOC
        df = avg_categories_by_ssoc[avg_categories_by_ssoc['year'].isin(['2018', '2021'])]
        df.sort_values(by=['SSOC4D', 'year'], ascending=True, inplace=True)
        df['2021-2018_diff'] = df['avg_tsc_category_count_per_job'].diff()
        df = df[df['year'] == '2021']
        df.drop(columns=['year'], inplace=True)

        filepath = self.analysis_filepath.format('avg_tsc_categories_change_by_ssoc')
        helper.save_csv(df, filepath)

    def tsc_categories_pdf(self):
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
        df = self.jobs[self.jobs['tsc_category_count'] != 0]
        df.sort_values(by=['year'], inplace=True)

        for year in df['year'].unique():
            temp = df[df['year'] == year]
            sns.kdeplot(temp['tsc_category_count'].tolist(), label=year, alpha=0.8)

        # Add labels
        plt.title('PDF of TSC Categories per Job Posting')
        plt.xlabel('Number of TSC Categories Required per Job Posting')
        plt.ylabel('Proportion of Job Postings')
        plt.legend(title='Year')

        filename = self.img_filepath.format('tsc_categories_pdf')
        plt.savefig(filename, transparent=True)
        plt.close()

    def tsc_categories_cdf(self):
        df = self.jobs[self.jobs['tsc_category_count'] != 0]
        df.sort_values(by=['year'], inplace=True)

        for year in df['year'].unique():
            temp = df[df['year'] == year]
            sns.kdeplot(temp['tsc_category_count'].tolist(), cumulative=True, label=year, alpha=0.8)

        # Add labels
        plt.title('CDF of TSC Categories per Job Posting')
        plt.xlabel('Number of TSC Categories Required per Job Posting')
        plt.ylabel('Proportion of Job Postings')
        plt.legend(title='Year')

        filename = self.img_filepath.format('tsc_categories_cdf')
        plt.savefig(filename, transparent=True)
        plt.close()

    def prop_jobs_per_tsc_category_in_ssoc(self):
        # get the tsc categories that each job requires
        self.jobs['tsc_category'] = self.jobs['tsc_category'].apply(ast.literal_eval)
        self.jobs['categories'] = self.jobs['tsc_category'].apply(lambda x: list(x.keys()))

        # get all unique categories
        categories = helper.get_all_unique_tsc_categories()

        # For each SSOC, get the prop of jobs in that SSOC requiring each tsc category by year
        df = pd.DataFrame(columns=['SSOC4D', 'ict', 'year', 'tsc_category'])
        for year in self.jobs['year'].unique():
            for ssoc in self.jobs['SSOC4D'].unique():
                temp = self.jobs[(self.jobs['year'] == year) & (self.jobs['SSOC4D'] == ssoc)]

                if not temp.empty:
                    ict_indicator = temp['ict'].unique()[0]

                    # total number of jobs in SSOC4d and year
                    num_postings = len(temp)

                    # for each tsc category, count the number of jobs requiring it
                    count_list = []
                    required_categories = sum(temp['categories'].tolist(), [])
                    for c in categories:
                        count = required_categories.count(c)
                        count_list.append(count)

                    temp_df = pd.DataFrame(
                        data={'SSOC4D': ssoc, 'year': year, 'tsc_category': categories,
                              'num_jobs_requiring_tsc_category_in_ssoc_year': count_list,
                              'total_jobs_in_ssoc_year': num_postings, 'ict': ict_indicator})

                else:
                    temp_df = pd.DataFrame(
                        data={'SSOC4D': ssoc, 'year': year, 'tsc_category': categories,
                              'num_jobs_requiring_tsc_category_in_ssoc_year': 0,
                              'total_jobs_in_ssoc_year': 0, 'ict': ssoc in self.ict_ssoc})

                df = df.append(temp_df, ignore_index=True)

        # get proportion of jobs requiring each tsc category in ssoc and year
        df['prop_jobs_requiring_tsc_category_in_ssoc_year'] = df['num_jobs_requiring_tsc_category_in_ssoc_year'] / df[
            'total_jobs_in_ssoc_year']

        filepath = self.analysis_filepath.format('prop_jobs_by_tsc_category')
        helper.save_csv(df, filepath)
        return df

    def change_prop_jobs_per_tsc_category_in_ssoc(self, prop_jobs_by_category):
        # get change per tsc category and ssoc from 2018 to 2021
        df = prop_jobs_by_category[prop_jobs_by_category['year'].isin(['2018', '2021'])]
        df.sort_values(by=['SSOC4D', 'tsc_category', 'year'], ascending=True, inplace=True)
        df['2021-2018_diff'] = df['prop_jobs_requiring_tsc_category_in_ssoc_year'].diff()
        df = df[df['year'] == '2021']
        df = df[['SSOC4D', 'ict', 'tsc_category', '2021-2018_diff']]

        filepath = self.analysis_filepath.format('prop_jobs_change_by_tsc_category')
        helper.save_csv(df, filepath)

    def skill_word_clouds(self):
        # get only some ssocs
        ssocs = [2512, 2152, 2511]
        df = self.jobs[self.jobs['SSOC4D'].isin(ssocs)]

        # get jobs in 2018 and 2021
        df = df[df['year'].isin(['2018', '2021'])]

        # get word clouds for each year and ssoc
        my_stopwords = ['will', 'well', 'able', 'required', 'provide']
        for ssoc in df['SSOC4D'].unique():
            for year in df['year'].unique():
                temp = df[(df['SSOC4D'] == ssoc) & (df['year'] == year)]

                # remove super light blues
                min_val, max_val = 0.3, 1.0
                n = 10
                colors = matplotlib.colors.LinearSegmentedColormap.from_list("mycmap",
                                                                             plt.cm.Blues(
                                                                                 np.linspace(min_val, max_val, n)))

                text = ' '.join(temp['JOB_POST_DESC']).lower()
                text = text.encode('ascii', 'ignore').decode()

                # Create a wordcloud and save to img folder
                plt.figure(figsize=(10, 8))
                wordcloud = WordCloud(max_words=50, background_color='white', prefer_horizontal=1, colormap=colors,
                                      width=2500, height=1500, stopwords=list(STOPWORDS) + my_stopwords).generate(text)
                plt.axis("off")

                wordcloud.to_file(self.img_filepath.format('ssoc{}_{}'.format(ssoc, year)))
                plt.close()
