import torch
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


class ConvertAbilitiesToBert:
    def __init__(self, ict_tsc_filepath, abilities_filepath, abilities_bert_filepath):
        self.ict_tsc_filepath = ict_tsc_filepath
        self.abilities_filepath = abilities_filepath
        self.abilities_bert_filepath = abilities_bert_filepath

    def run(self):
        tsc = pd.read_csv(self.ict_tsc_filepath)

        abilities_list = self.get_unique_abilities(tsc)
        self.convert_abilities_to_bert(abilities_list)

    def get_unique_abilities(self, tsc_df):
        # prep abilities list
        tsc_df['abilities_list'] = tsc_df['abilities_list'].apply(
            lambda x: [i.strip(" '") for i in x.strip('[]').split("',")])

        # get list of unique abilities among ICT TSCs
        abilities = list(set(sum(tsc_df['abilities_list'].tolist(), [])))
        df = pd.DataFrame(data={'ability': abilities})
        df.to_csv(self.abilities_filepath, index=False)

        return abilities

    def convert_abilities_to_bert(self, abilities_list):
        print('Converting {} abilities of digital skills'.format(len(abilities_list)))

        # Activate GPU if any
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        model = SentenceTransformer('all-distilroberta-v1').to(device)

        # convert to BERT
        sentence_embeddings = model.encode(abilities_list).tolist()

        # save as npy file
        sentence_embeddings = np.asarray(sentence_embeddings)
        np.save(self.abilities_bert_filepath, sentence_embeddings)
