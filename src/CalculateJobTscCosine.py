import os
import helper
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import MultiLabelBinarizer


class CalculateJobTscCosine:
    def __init__(self, abilities_filepath, ict_tsc_filepath, job_bert_folder, job_ability_cosine_filepath,
                 job_tsc_cosine_filepath):
        self.abilities_filepath = abilities_filepath
        self.ict_tsc_filepath = ict_tsc_filepath
        self.job_postings_folder = job_bert_folder
        self.job_ability_cosine_filepath = job_ability_cosine_filepath
        self.job_tsc_cosine_filepath = job_tsc_cosine_filepath

        self.booleans = None
        self.tsc_ability_matrix = None
        self.abilities = pd.DataFrame()
        self.tsc = pd.DataFrame()

    def run(self):
        startTime = datetime.now()

        self.read_data()
        self.get_tsc_abilities_matrix()

        for i in os.listdir(self.job_postings_folder):
            print('Processing file {}'.format(i))
            base_filename = i.split('.')[0]

            # read job-ability cosine similarity file
            cosine_filepath = self.job_ability_cosine_filepath.format(base_filename)
            cosine_matrix = np.load(cosine_filepath)

            # get job-tsc cosine similarity
            job_tsc_cosine = self.get_job_tsc_cosine(cosine_matrix)

            # matrix columns will be ordered in this manner: self.tsc['tsc_proficiency'].tolist()
            output_path = self.job_tsc_cosine_filepath.format(base_filename)
            np.save(output_path, job_tsc_cosine)

        print(datetime.now() - startTime)

    def read_data(self):
        self.abilities = pd.read_csv(self.abilities_filepath)
        self.tsc = pd.read_csv(self.ict_tsc_filepath)

        # filter out some tsc categories
        self.tsc = helper.get_ict_skills(self.tsc)
        self.tsc['tsc_proficiency'] = list(zip(self.tsc['tsc_title'], self.tsc['proficiency_level']))

        # prep abilities
        self.tsc['abilities_clean'] = self.tsc['abilities_list'].apply(helper.clean_abilities)

    def get_tsc_abilities_matrix(self):
        print('Getting a boolean matrix of abilities in each TSC')

        # get a (no. of abilities) x (no. of tsc-profs) matrix containing 1 and 0, 1 if an ability is needed for a tsc
        abilities = self.abilities['ability'].tolist()

        # create booleans
        mlb = MultiLabelBinarizer()
        booleans = pd.DataFrame(mlb.fit_transform(self.tsc['abilities_clean']), columns=mlb.classes_,
                                index=self.tsc['tsc_proficiency'])

        # rearrange columns so that abilities are in the right order
        self.booleans = booleans[abilities]

        # transpose to get our matrix (col=tsc proficiency, row=ability)
        self.tsc_ability_matrix = np.asarray(self.booleans.transpose())

    def get_job_tsc_cosine(self, cosine_matrix):
        print('Getting average cosine similarity score for each TSC and job')

        # multiply matrices to get a (no. of jobs) x (no. of tsc-profs) matrix, with each element being the sum of
        # job_ability_cosine scores among a TSC's abilities for a particular job
        cosine_sum_matrix = np.matmul(cosine_matrix, self.tsc_ability_matrix)

        # get a vector with element i being the number of abilities that TSC i has
        tsc_ability_count_vector = self.tsc_ability_matrix.sum(axis=0)

        # divide to get average job_ability_cosine score between each tsc and each job
        avg_cosine_matrix = cosine_sum_matrix / tsc_ability_count_vector

        return avg_cosine_matrix
