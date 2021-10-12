import pandas as pd
import torch
import helper
from sentence_transformers import SentenceTransformer


class ConvertAbilitiesToBert:
    def __init__(self, ict_tsc_filepath, output_filepath):
        self.ict_tsc_filepath = ict_tsc_filepath
        self.output_filepath = output_filepath

        self.tsc = pd.DataFrame()
        self.abilities = []

    def run(self):
        self.tsc = pd.read_csv(self.ict_tsc_filepath)
        self.tsc = helper.get_ict_skills(self.tsc)

        self.get_unique_abilities()
        self.convert_abilities_to_bert()

    def get_unique_abilities(self):
        # prep abilities list
        self.tsc['abilities_clean'] = self.tsc['abilities_list'].apply(helper.clean_abilities)

        # get list of unique abilities among ICT TSCs
        self.abilities = list(set(sum(self.tsc['abilities_clean'].tolist(), [])))

    def convert_abilities_to_bert(self):
        # Activate GPU if any
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        model = SentenceTransformer('all-distilroberta-v1').to(device)

        # convert to BERT
        embeddings_list = []
        for index, text in enumerate(self.abilities):
            print('Converting ability {} out of {}'.format(index + 1, len(self.abilities)))

            # get sentence embedding
            sentence_embeddings = model.encode(text).tolist()

            embeddings_list.append(sentence_embeddings)

        abilities_df = pd.DataFrame(data={'ability': self.abilities, 'bert_embeddings': embeddings_list})
        abilities_df.to_csv(self.output_filepath, index=False)
