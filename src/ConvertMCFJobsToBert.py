import pandas as pd
from transformers import BertTokenizer, BertModel
import os
import helper

"""
This class converts each MCF job posting description
into a word embedding vector of 768 elements using BERT.
"""


class ConvertMCFJobsToBert:
    def __init__(self, postings_dir, output_filepath):
        self.postings_dir = postings_dir
        self.output_filepath = output_filepath

        self.tokenizer = None
        self.model = None

    def run(self):
        self.init_bert()
        self.desc_to_bert()

    def init_bert(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased', output_hidden_states=True)

    def desc_to_bert(self):
        for i in os.listdir(self.postings_dir):
            filepath = self.postings_dir + i
            filename_base = '_'.join(i.split('_')[:-1])
            print(filename_base)

            # read file
            df = pd.read_csv(filepath)
            df.drop_duplicates(inplace=True)

            # get job posting descriptions
            jobdesc = df['JOB_POST_DESC'].tolist()
            totaljobs = len(jobdesc)

            # get bert embeddings for each job posting description
            embeddings_list = []
            for index, text in enumerate(jobdesc):
                tokenized_text, tokens_tensor, segments_tensors = helper.bert_text_preparation(text, self.tokenizer)
                job_embeddings = helper.get_bert_embeddings(tokens_tensor, segments_tensors, self.model)

                print('Job {} out of {} done for {} - {} x 1 vector embedding'.format(index + 1, totaljobs, i,
                                                                                             len(job_embeddings)))
                embeddings_list.append(job_embeddings)

            df['bert_embeddings'] = embeddings_list

            df.to_csv(self.output_filepath.format(filename_base),index=False)
