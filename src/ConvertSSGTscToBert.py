import pandas as pd
import ast
import torch
from transformers import BertTokenizer, BertModel
from datetime import datetime

"""
This class converts each TSC-proficiency under the SSG Skills Framework
into a word embedding vector of 768 elements using BERT.
"""


class ConvertSSGTscToBert:
    def __init__(self, tsc_items_filepath, output_filepath):
        self.input_filepath = tsc_items_filepath
        self.output_filepath = output_filepath

        self.tsc = pd.DataFrame()
        self.tokenizer = None
        self.model = None

    def run(self):
        startTime = datetime.now()

        self.init_bert()
        self.tsc = pd.read_csv(self.input_filepath)
        abilities = self.get_abilities_list()
        self.tsc_to_bert(abilities)

        print(datetime.now() - startTime)

    def init_bert(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

    def get_abilities_list(self):
        # Get 1 list of abilities for 1 TSC
        abilities_list = self.tsc['abilities_list'].apply(lambda x: ast.literal_eval(x))

        # Combine each list of abilities to get 1 abilities string for 1 TSC
        abilities_str = [' '.join(x) for x in abilities_list]

        return abilities_str

    def tsc_to_bert(self, abilities_str):
        # Activate GPU if any
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model = self.model.to(device)

        embeddings_list = []
        for index, text in enumerate(abilities_str):
            inputs = self.tokenizer(text, return_tensors="pt").to(device)
            outputs = self.model(**inputs)
            last_hidden_states = outputs.last_hidden_state

            # get avg embedding across tokens
            embeddings = torch.mean(last_hidden_states[0], dim=0).to(device)
            list_embeddings = [e.tolist() for e in embeddings]

            print('TSC {} done - {} x 1 vector embedding'.format(index + 1, len(list_embeddings)))
            embeddings_list.append(list_embeddings)

        self.tsc['bert_embeddings'] = embeddings_list
        self.tsc.to_csv(self.output_filepath, index=False)
