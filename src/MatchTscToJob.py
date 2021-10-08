import os
import helper
import pandas as pd
import numpy as np
from datetime import datetime
from collections import Counter


class MatchTscToJob:
    def __init__(self, ict_tsc_filepath, job_postings_folder, job_tsc_cosine_filepath, jobs_final_filepath,
                 cosine_threshold=0):
        self.ict_tsc_filepath = ict_tsc_filepath
        self.job_postings_folder = job_postings_folder
        self.job_tsc_cosine_filepath = job_tsc_cosine_filepath
        self.jobs_final_filepath = jobs_final_filepath
        self.cosine = cosine_threshold

        self.tsc = pd.DataFrame()

    def run(self):
        startTime = datetime.now()

        self.read_data()

        for i in os.listdir(self.job_postings_folder):
            print('Processing file {}'.format(i))
            base_filename = i.split('.')[0]

            # read job postings file
            postings_filepath = self.job_postings_folder + i
            print(postings_filepath)
            jobs_df = pd.read_csv(postings_filepath)

            # read job-tsc cosine similarity file
            cosine_filepath = self.job_tsc_cosine_filepath.format(base_filename + '_bert')
            print(cosine_filepath)
            cosine_df = pd.DataFrame(np.load(cosine_filepath), columns=self.tsc['tsc_proficiency'].tolist())

            # match tscs to jobs
            jobs_df = self.match_tsc_to_jobs(cosine_df, jobs_df)
            jobs_df = self.match_tsc_to_category(jobs_df)

            output_path = self.jobs_final_filepath.format(base_filename)
            jobs_df.to_csv(output_path, index=False)

        print(datetime.now() - startTime)

    def read_data(self):
        self.tsc = pd.read_csv(self.ict_tsc_filepath)

        # filter out some tsc categories
        self.tsc = helper.get_ict_skills(self.tsc)
        self.tsc['tsc_proficiency'] = list(zip(self.tsc['tsc_title'], self.tsc['proficiency_level']))

        # prep abilities
        self.tsc['abilities_clean'] = self.tsc['abilities_list'].apply(helper.clean_abilities)

    def match_tsc_to_jobs(self, job_tsc_cosine, jobs_df):
        print('Getting TSCs that pass threshold for each job')

        # for each job, get a list of TSC-profs that have an avg job_ability_cosine similarity higher than the threshold
        job_tscs = list(np.where(job_tsc_cosine.gt(self.cosine, axis=0), job_tsc_cosine.columns, ''))
        job_tscs = [[i for i in x if i != ''] for x in job_tscs]
        jobs_df['tsc_list'] = job_tscs
        jobs_df['tsc_count'] = jobs_df['tsc_list'].apply(len)

        return jobs_df

    def match_tsc_to_category(self, jobs_df):
        print('Mapping TSCs to TSC categories for each job')

        # get a dict where key = tsc proficiency and value = tsc category
        tsc_category_dict = pd.Series(self.tsc['tsc_category'].values, index=self.tsc['tsc_proficiency']).to_dict()

        # map tsc to category
        category_list = [[tsc_category_dict[i] for i in x] for x in jobs_df['tsc_list']]
        category_counter = [dict(Counter(x)) for x in category_list]
        jobs_df['tsc_category'] = category_counter
        jobs_df['tsc_category_count'] = jobs_df['tsc_category'].apply(lambda x: len(x.keys()))

        return jobs_df
