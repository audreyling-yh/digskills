import os
import pandas as pd
import numpy as np
import config
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
        self.jobs = helper.indicate_ict_job(self.jobs)

        # get tsc metrics
        count_jobs_by_ssoc = self.count_jobs_by_ssoc()
        avg_tsc_by_ssoc = self.avg_tsc_per_job_in_ssoc(count_jobs_by_ssoc)
        self.change_avg_tsc_per_job_in_ssoc(avg_tsc_by_ssoc)

        # get evolution in proportion of jobs requiring each tsc
        prop_jobs_by_tsc = self.prop_jobs_per_tsc_in_ssoc(count_jobs_by_ssoc)
        self.change_prop_jobs_per_tsc_in_ssoc(prop_jobs_by_tsc)

        # get TSC cdf
        self.tsc_pdf_cdf(cdf=True)
        self.tsc_pdf_cdf(type='ict', cdf=True)
        self.tsc_pdf_cdf(type='nonict', cdf=True)

        # evolution in proportion of jobs requiring each programming languages
        self.prop_programming_in_ssoc_year(count_jobs_by_ssoc)
        self.prop_programming_count_in_ssoc_year(count_jobs_by_ssoc)
        count_programming_by_ssoc = self.count_programming_language_in_ssoc()
        self.prop_programming_language_in_ssoc(count_jobs_by_ssoc, count_programming_by_ssoc)

        # job description word clouds
        self.overall_word_clouds()

    def count_jobs_by_ssoc(self):
        # count the total number of jobs per ssoc per year
        df = self.jobs.groupby(['SSOC 2020', 'ict', 'year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'total_jobs'}, inplace=True)

        return df

    def avg_tsc_per_job_in_ssoc(self, count_jobs_by_ssoc):
        # For each SSOC, get the average number of tscs per job posting per year
        df = self.jobs.groupby(['SSOC 2020', 'ict', 'year'])['tsc_count'].mean().reset_index()
        df.rename(columns={'tsc_count': 'avg_tsc_count_per_job'}, inplace=True)

        # get total number of jobs
        df = df.merge(count_jobs_by_ssoc, on=['SSOC 2020', 'ict', 'year'])

        filepath = self.analysis_filepath.format('avg_tsc_by_ssoc')
        helper.save_csv(df, filepath)
        return df

    def change_avg_tsc_per_job_in_ssoc(self, avg_tsc_by_ssoc):
        # get 2021-2018 change in avg tscs per job per SSOC
        df = pd.pivot_table(avg_tsc_by_ssoc, index=['SSOC 2020', 'ict'], columns='year',
                            values='avg_tsc_count_per_job').reset_index()
        df.index.name = None
        df.fillna(0, inplace=True)
        df['2021-2018_diff'] = df['2021'] - df['2018']

        filepath = self.analysis_filepath.format('avg_tsc_change_by_ssoc')
        helper.save_csv(df, filepath)

    def tsc_pdf_cdf(self, type=None, cdf=True):
        # create pdf/cdf of number of tscs per job postings
        sns.set(style='ticks')
        os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
        df = self.jobs.sort_values(by=['year'])

        # configuration
        if type == 'ict':
            df = df[df['ict']]
            type_str = 'ict_'
            graph_annotation = ' (ICT Occupations)'
        elif type == 'nonict':
            df = df[~df['ict']]
            type_str = 'nonict_'
            graph_annotation = ' (Non-ICT Occupations)'
        else:
            type_str, graph_annotation = '', ''

        # get cdf/pdf
        for year in df['year'].unique():
            temp = df[df['year'] == year]
            sns.kdeplot(temp['tsc_count'].tolist(), cumulative=cdf, label=year, alpha=0.8)

        plt.xlim(xmin=0)
        plt.ylim([0, 1.1])

        # Add labels
        title = 'CDF' if cdf else 'PDF'
        plt.title('{} of TSCs per Job Posting{}'.format(title, graph_annotation))
        plt.xlabel('Number of TSCs Required per Job Posting')
        plt.ylabel('Proportion of Job Postings')
        plt.legend(title='Year')

        filename = self.img_filepath.format('tsc_{}{}'.format(type_str, title))
        plt.savefig(filename, transparent=True)
        plt.close()

    def prop_jobs_per_tsc_in_ssoc(self, count_jobs_by_ssoc):
        # drop jobs without tsc
        df = self.jobs[self.jobs['tsc_count'] > 0]

        # within each SSOC, count the number of jobs requiring each tsc (without prof level) by year
        df['tsc_list'] = df['tsc_list'].apply(lambda x: list(set([i[0] for i in x])))
        df = df.explode('tsc_list')
        df = df.groupby(['SSOC 2020', 'year', 'tsc_list'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'tsc_list': 'tsc', 'JOB_POST_ID': 'num_jobs_requiring_tsc_in_ssoc_year'}, inplace=True)

        # merge
        df = df.merge(count_jobs_by_ssoc, on=['SSOC 2020', 'year'])
        df.fillna(0, inplace=True)

        # get proportion of jobs requiring each tsc in ssoc and year
        df['prop_jobs_requiring_tsc_in_ssoc_year'] = df['num_jobs_requiring_tsc_in_ssoc_year'] / df['total_jobs']

        filepath = self.analysis_filepath.format('prop_jobs_by_tsc')
        helper.save_csv(df, filepath)
        return df

    def change_prop_jobs_per_tsc_in_ssoc(self, prop_jobs_by_tsc):
        # get 2021-2018 change in prop of jobs per tsc and ssoc
        df = pd.pivot_table(prop_jobs_by_tsc, index=['SSOC 2020', 'tsc', 'ict'], columns='year',
                            values='prop_jobs_requiring_tsc_in_ssoc_year').reset_index()
        df.index.name = None
        df.fillna(0, inplace=True)
        df['2021-2018_diff'] = df['2021'] - df['2018']

        filepath = self.analysis_filepath.format('prop_jobs_change_by_tsc')
        helper.save_csv(df, filepath)

    def prop_programming_in_ssoc_year(self, count_jobs_by_ssoc):
        # count number of jobs requiring at least 1 programming language by ssoc and year
        df = self.jobs[self.jobs['pl_count'] > 0]
        df = df.groupby(['SSOC 2020', 'year'])['JOB_POST_DESC'].count().reset_index()
        df.rename(columns={'JOB_POST_DESC': 'num_jobs_requiring_programming'}, inplace=True)

        # get proportion of jobs requiring at least 1 programming language by ssoc and year
        df = df.merge(count_jobs_by_ssoc, on=['SSOC 2020', 'year'])
        df['prop_jobs_requiring_programming'] = df['num_jobs_requiring_programming'] / df['total_jobs']

        filepath = self.analysis_filepath.format('prop_programming_by_ssoc')
        helper.save_csv(df, filepath)

    def prop_programming_count_in_ssoc_year(self, count_jobs_by_ssoc):
        # count number of jobs requiring at each number of programming languages by ssoc and year
        df = self.jobs[self.jobs['pl_count'] > 0]
        df = df.groupby(['SSOC 2020', 'year', 'pl_count'])['JOB_POST_DESC'].count().reset_index()
        df.rename(columns={'JOB_POST_DESC': 'num_jobs_requiring_num_programming_lang'}, inplace=True)

        # get proportion of jobs requiring each no. of programming languages by ssoc and year
        df = df.merge(count_jobs_by_ssoc, on=['SSOC 2020', 'year'])
        df['prop_jobs_requiring_num_programming_lang'] = df['num_jobs_requiring_num_programming_lang'] / df[
            'total_jobs']

        filepath = self.analysis_filepath.format('prop_num_programming_language_by_ssoc')
        helper.save_csv(df, filepath)

    def count_programming_language_in_ssoc(self):
        # drop jobs without programming languages
        df = self.jobs[self.jobs['pl_count'] > 0]

        # for each ssoc and year, get the freq count of each programming language
        df = df.explode('programming_languages')
        df = df.groupby(['SSOC 2020', 'year', 'programming_languages'])['JOB_POST_DESC'].count().reset_index()
        df.rename(columns={'JOB_POST_DESC': 'count'}, inplace=True)

        return df

    def prop_programming_language_in_ssoc(self, count_jobs_by_ssoc, count_programming_by_ssoc):
        # merge the 2 dfs
        df = count_jobs_by_ssoc.merge(count_programming_by_ssoc, on=['SSOC 2020', 'year'])

        # get proportion of jobs in ssoc requiring each programming language
        df['prop_jobs_requiring_programming_language_in_ssoc_year'] = df['count'] / df['total_jobs']

        filepath = self.analysis_filepath.format('prop_programming_language_by_ssoc')
        helper.save_csv(df, filepath)

    def overall_word_clouds(self):
        # set font
        fontpath = 'C://Windows/Fonts/Arial.ttf'

        # get only specific ssocs
        ssocs = [21222, 21664, 24213, 25111, 25121]
        df = self.jobs[self.jobs['SSOC 2020'].isin(ssocs)]

        # get jobs in 2018 and 2021
        df = df[df['year'].isin(['2018', '2021'])]

        # set different colors for dif years
        min_val, max_val = 0.3, 1.0
        n = 10
        colors = {
            '2018': matplotlib.colors.LinearSegmentedColormap.from_list("mycmap",
                                                                        plt.cm.Blues(np.linspace(min_val, max_val, n))),
            '2021': matplotlib.colors.LinearSegmentedColormap.from_list("mycmap", plt.cm.Purples(
                np.linspace(min_val, max_val, n))),
        }

        # get word clouds for each year and ssoc
        year_list = df['year'].unique()
        combination_list = [(ssoc, year) for ssoc in ssocs for year in year_list]
        for (ssoc, year) in combination_list:
            temp = df[(df['SSOC 2020'] == ssoc) & (df['year'] == year)]

            text = ' '.join(temp['JOB_POST_DESC']).lower()
            text = text.encode('ascii', 'ignore').decode()

            # Create a wordcloud and save to img folder
            plt.figure(figsize=(10, 8))
            wordcloud = WordCloud(max_words=50, background_color='white', prefer_horizontal=1, colormap=colors[year],
                                  width=2500, height=1500, stopwords=list(STOPWORDS) + config.my_stopwords,
                                  font_path=fontpath).generate(text)
            plt.axis("off")

            filepath = self.img_filepath.format('desc_ssoc{}_{}'.format(ssoc, year))
            wordcloud.to_file(filepath)
            plt.close()
