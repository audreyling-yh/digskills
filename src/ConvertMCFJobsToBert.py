import pandas as pd
import os
import torch
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer


class ConvertMCFJobsToBert:
    def __init__(self, postings_dir, output_filepath):
        self.postings_dir = postings_dir
        self.output_filepath = output_filepath

    def run(self):
        startTime = datetime.now()
        self.desc_to_bert()
        print(datetime.now() - startTime)

    def desc_to_bert(self):
        for i in os.listdir(self.postings_dir):
            filepath = self.postings_dir + i
            filename_base = i.split('.')[0]
            print(filename_base)

            # read file
            df = pd.read_csv(filepath)

            # get job posting descriptions
            jobdesc = df['JOB_POST_DESC'].tolist()
            totaljobs = len(jobdesc)

            # Activate GPU if any
            device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
            model = SentenceTransformer('paraphrase-distilroberta-base-v1').to(device)

            embeddings_list = []
            for index, text in enumerate(jobdesc):
                # get sentence embeddings
                text=text.split('.')
                sentence_embeddings = model.encode(text)

                # get avg embedding across sentences
                embeddings = np.mean(sentence_embeddings, axis=0)

                embeddings_list.append(embeddings)

                print('Job {} out of {} done for {} - {} x 1 vector embedding'.format(index + 1, totaljobs, i,
                                                                                      len(embeddings)))

            embeddings_list = np.asarray(embeddings_list)

            output_path = self.output_filepath.format(filename_base)
            np.save(output_path, embeddings_list)
