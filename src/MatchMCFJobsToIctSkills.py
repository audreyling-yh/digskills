import pandas as pd
import ast
import numpy as np
import os


class MatchMCFJobsToIctSkills:
    def __init__(self, ict_tsc_filepath, job_postings_folder, cosine_matrix_outputpath, job_tsc_outputpath):
        self.ict_tsc_filepath = ict_tsc_filepath
        self.job_postings_folder = job_postings_folder
        self.cosine_matrix_outputpath = cosine_matrix_outputpath
        self.job_tsc_outputpath = job_tsc_outputpath

        self.tsc = None

    def run(self):
        self.tsc = pd.read_csv(self.ict_tsc_filepath)
        self.tsc['bert_embeddings'] = self.tsc['bert_embeddings'].apply(lambda x: np.array(ast.literal_eval(x)))
        self.tsc.drop_duplicates(subset=['tsc_id_proficiency_level'], inplace=True)  # get unique tsc-profs

        for i in os.listdir(self.job_postings_folder):
            print(i)
            filepath = self.job_postings_folder + i
            jobs = pd.read_csv(filepath)
            jobs['bert_embeddings'] = jobs['bert_embeddings'].apply(lambda x: np.array(ast.literal_eval(x)))

            filename = i.split('.')[0]

            # Get cosine similarity scores
            os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
            cosine = self.get_cosine_similarity_matrix(jobs)
            cosine.to_csv(self.cosine_matrix_outputpath.format(filename), index=True)

            # For each job, get a list of TSC-profs that have cosine sim above threshold
            jobs_updated = self.get_tscs_for_jobs(jobs, cosine, cosine_threshold=0.85)
            jobs_updated.to_csv(self.job_tsc_outputpath.format(filename), index=False)

    def get_cosine_similarity_matrix(self, jobs):
        job_embeddings = np.row_stack(jobs['bert_embeddings'])  # no. of jobs x 768 matrix
        tsc_embeddings = np.column_stack(self.tsc['bert_embeddings'])  # 768 x no. of TSCs

        dpmatrix = self.get_dot_product_matrix(job_embeddings, tsc_embeddings)
        magmatrix = self.get_magnitude_matrix(job_embeddings, tsc_embeddings)

        cosinematrix = dpmatrix / magmatrix
        cosine_df = pd.DataFrame(cosinematrix)
        cosine_df.columns = self.tsc['tsc_id_proficiency_level']

        return cosine_df

    def get_dot_product_matrix(self, job_embeddings, tsc_embeddings):
        print('Getting dot product matrix...')
        matrix = np.matmul(job_embeddings, tsc_embeddings)  # dot product matrix - no. of jobs x no. of TSCs
        return matrix

    def get_magnitude_matrix(self, job_embeddings, tsc_embeddings):
        print('Getting magnitude matrix...')
        job_squared = job_embeddings ** 2
        job_squared = np.row_stack(np.sqrt(job_squared.sum(axis=1)))  # no. of jobs x 1 matrix
        tsc_squared = np.transpose(tsc_embeddings ** 2)
        tsc_squared = np.column_stack(np.vstack(np.sqrt(tsc_squared.sum(axis=1))))  # 1 x no. of TSCs matrix
        matrix = np.matmul(job_squared, tsc_squared)  # magnitude matrix - no. of jobs x no. of elements
        return matrix

    def get_tscs_for_jobs(self, jobs, cosine_df, cosine_threshold=0.85):
        print('Getting skills above cosine threshold...')
        job_tscs = (cosine_df > cosine_threshold).apply(lambda x: cosine_df.columns[x.tolist()].tolist(), axis=1)
        jobs['skill_list'] = job_tscs
        return jobs
