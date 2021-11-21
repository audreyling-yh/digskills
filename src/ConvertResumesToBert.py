import os
import torch
import pandas as pd
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer


class ConvertResumesToBert:
    def __init__(self, resumes_folder, output_filepath):
        self.resumes_folder = resumes_folder
        self.output_filepath = output_filepath

    def run(self):
        startTime = datetime.now()
        self.res_to_bert()
        print(datetime.now() - startTime)

    def res_to_bert(self):
        for i in os.listdir(self.resumes_folder):
            filepath = self.resumes_folder + i
            filename_base = i.split('.')[0]
            print(filename_base)

            # read file
            df = pd.read_csv(filepath)

            # get month's resumes
            resumes = df['resume'].tolist()
            totalresumes = len(resumes)

            # Activate GPU if any
            device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
            model = SentenceTransformer('all-distilroberta-v1').to(device)

            embeddings_list = []
            for index, text in enumerate(resumes):
                # get sentence embeddings
                text = text.split('.')
                sentence_embeddings = model.encode(text)

                # get avg embedding across sentences
                embeddings = np.mean(sentence_embeddings, axis=0)

                embeddings_list.append(embeddings)

                print(
                    'Resume {} out of {} done for {} - {} x 1 vector embedding'.format(index + 1, totalresumes,
                                                                                       filename_base, len(embeddings)))

            embeddings_list = np.asarray(embeddings_list)

            output_path = self.output_filepath.format(filename_base)
            np.save(output_path, embeddings_list)
