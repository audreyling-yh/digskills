import pandas as pd
import ast
import os
import numpy as np
from datetime import datetime


class CalculateJobAbilityCosine:
    def __init__(self, abilities_filepath, job_bert_folder, cosine_matrix_outputpath):
        self.abilities_filepath = abilities_filepath
        self.job_postings_folder = job_bert_folder
        self.cosine_matrix_outputpath = cosine_matrix_outputpath

        self.abilities = pd.DataFrame()

    def run(self):
        startTime = datetime.now()

        self.read_data()

        for i in os.listdir(self.job_postings_folder):
            print('Processing file {}'.format(i))
            base_filename = i.split('.')[0]

            # get job embeddings
            filepath = self.job_postings_folder + i
            job_embeddings = np.load(filepath)

            # Get job_ability_cosine similarity scores
            os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
            cosine = self.get_cosine_similarity_matrix(job_embeddings)

            # matrix columns will be ordered in this manner: self.abilities['ability'].tolist()
            output_path = self.cosine_matrix_outputpath.format(base_filename)
            np.save(output_path, cosine)

        print(datetime.now() - startTime)

    def read_data(self):
        self.abilities = pd.read_csv(self.abilities_filepath)
        self.abilities['bert_embeddings'] = self.abilities['bert_embeddings'].apply(ast.literal_eval)

    def get_cosine_similarity_matrix(self, job_embeddings):
        # jobs_embeddings is a (no. of jobs) x 768 matrix
        ability_embeddings = np.column_stack(
            np.asarray(self.abilities['bert_embeddings'].tolist()))  # 768 x (no. of abilities)

        dpmatrix = self.get_dot_product_matrix(job_embeddings, ability_embeddings)
        magmatrix = self.get_magnitude_matrix(job_embeddings, ability_embeddings)

        cosinematrix = dpmatrix / magmatrix

        return cosinematrix

    def get_dot_product_matrix(self, job_embeddings, ability_embeddings):
        print('Getting dot product matrix...')
        matrix = np.matmul(job_embeddings, ability_embeddings)  # dot product matrix: (no. of jobs) x (no. of abilities)
        return matrix

    def get_magnitude_matrix(self, job_embeddings, ability_embeddings):
        print('Getting magnitude matrix...')
        job_squared = job_embeddings ** 2
        job_squared = np.sqrt(job_squared.sum(axis=1))[np.newaxis, :].T  # (no. of jobs) x 1 matrix
        abilities_squared = np.transpose(ability_embeddings ** 2)
        abilities_squared = np.column_stack(
            np.vstack(np.sqrt(abilities_squared.sum(axis=1))))  # 1 x (no. of abilities) matrix
        matrix = np.matmul(job_squared, abilities_squared)  # magnitude matrix - (no. of jobs) x (no. of elements)
        return matrix
