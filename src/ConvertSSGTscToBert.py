import pandas as pd
import ast
import helper
import torch
from transformers import BertTokenizer, BertModel

"""
This class converts each TSC-proficiency under the SSG Skills Framework
into a word embedding vector of 768 elements using BERT.
"""


class ConvertSSGTscToBert:
    def __init__(self, tsc_items_filepath, output_filepath):
        self.input_filepath = tsc_items_filepath
        self.output_filepath = output_filepath

        self.tokenizer = None
        self.model = None

    def run(self):
        self.init_bert()
        tsc = pd.read_csv(self.input_filepath)
        abilities = self.get_abilities_list(tsc)
        embeddings = self.tsc_to_bert(abilities)
        self.save_embeddings(tsc, embeddings, self.output_filepath)

    def init_bert(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

    def get_abilities_list(self, df):
        # Get 1 list of abilities for 1 TSC
        abilities_list = df['abilities_list'].apply(lambda x: ast.literal_eval(x))

        # Combine each list of abilities to get 1 abilities string for 1 TSC
        abilities_str = [' '.join(x) for x in abilities_list]

        return abilities_str

    def tsc_to_bert(self, abilities_str):
        # Activate GPU if any
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

        embeddings_list = []
        for index, text in enumerate(abilities_str):

            # TODO: try out
            inputs = self.tokenizer(text, return_tensors="pt").to(device)
            outputs = self.model(**inputs)
            last_hidden_states = outputs.last_hidden_state

            # tokenized_text, tokens_tensor, segments_tensors = helper.bert_text_preparation(text, self.tokenizer)
            # tsc_embeddings = helper.get_bert_embeddings(tokens_tensor, segments_tensors, self.model)

            print('TSC {} done - {} x 1 vector embedding'.format(index + 1, len(last_hidden_states)))
            embeddings_list.append(tsc_embeddings)

        return embeddings_list

    def save_embeddings(self, df, embeddings, output_filepath):
        df['bert_embeddings'] = embeddings
        df.to_csv(output_filepath, index=False)
