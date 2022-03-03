import torch
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


class ConvertICTRolesToBert:
    def __init__(self, ict_roles_filepath, ict_roles_bert_filepath):
        self.ict_roles_filepath = ict_roles_filepath
        self.role_bert_filepath = ict_roles_bert_filepath

    def run(self):
        df = pd.read_csv(self.ict_roles_filepath)
        job_descriptions = df['job_role_description'].tolist()
        self.convert_roles_to_bert(job_descriptions)

    def convert_roles_to_bert(self, desc_list):
        print('Converting {} ICT job roles'.format(len(desc_list)))

        # Activate GPU if any
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        model = SentenceTransformer('all-distilroberta-v1').to(device)

        # convert to BERT
        sentence_embeddings = model.encode(desc_list).tolist()

        # save as npy file
        sentence_embeddings = np.asarray(sentence_embeddings)
        np.save(self.role_bert_filepath, sentence_embeddings)
