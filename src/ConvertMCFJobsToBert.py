import os
import vaex
import torch
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer


class ConvertMCFJobsToBert:
    def __init__(self, mcf_processed_folder, mcf_bert_folder, mcf_bert_filepath, overwrite=False):
        self.mcf_processed_folder = mcf_processed_folder
        self.mcf_bert_folder = mcf_bert_folder
        self.mcf_bert_filepath = mcf_bert_filepath
        self.overwrite = overwrite

    def run(self):
        start_time = datetime.now()

        files = [x for x in os.listdir(self.mcf_processed_folder)]

        # if true, overwrite all existing bert files; re-process
        if not self.overwrite:
            print('NOT overwriting existing bert files')
            existing_bert_files = [x.replace('.npy', '.hdf5') for x in os.listdir(self.mcf_bert_folder)]
            files = [x for x in files if x not in existing_bert_files]

        # loop for each month
        for i in files:
            month = i.split('.')[0].replace('jobsbank_', '')
            print('Converting {} job postings to bert'.format(month))

            filepath = self.mcf_processed_folder + i

            # get job descriptions
            df = vaex.open(filepath)
            df['JOB_POST_DESC'] = df['JOB_POST_DESC'].str.split('.')
            jd = df['JOB_POST_DESC'].tolist()

            # convert job descriptions to bert
            self.desc_to_bert(jd, i.split('.')[0])

        print(datetime.now() - start_time)

    def desc_to_bert(self, jd_list, month):
        # Activate GPU if any
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        model = SentenceTransformer('all-distilroberta-v1').to(device)

        total = len(jd_list)
        embeddings_list = []
        for index, sentences in enumerate(jd_list):
            # get sentence embeddings
            sentence_embeddings = model.encode(sentences)

            # get avg embedding across sentences
            embeddings = np.mean(sentence_embeddings, axis=0)

            embeddings_list.append(embeddings)

            print('\tJob {} out of {} done for {}'.format(index + 1, total, month))

        embeddings_list = np.asarray(embeddings_list)

        # save as npy file
        np.save(self.mcf_bert_filepath.format(month), embeddings_list)
