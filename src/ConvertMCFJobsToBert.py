import pandas as pd
from transformers import BertTokenizer, BertModel
import os
import torch
from datetime import datetime

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
        startTime = datetime.now()

        self.init_bert()
        self.desc_to_bert()

        print(datetime.now() - startTime)

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

            # clean file
            df.drop_duplicates(inplace=True)
            df.dropna(subset=['JOB_POST_DESC'],inplace=True)

            # get job posting descriptions
            jobdesc = df['JOB_POST_DESC'].tolist()
            totaljobs = len(jobdesc)

            # Activate GPU if any
            device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
            self.model = self.model.to(device)

            embeddings_list = []
            for index, text in enumerate(jobdesc):
                inputs = self.tokenizer(text, return_tensors="pt", truncation=True).to(device)
                outputs = self.model(**inputs)
                last_hidden_states = outputs.last_hidden_state

                # get avg embedding across tokens
                embeddings = torch.mean(last_hidden_states[0], dim=0).to(device)
                job_embeddings = [e.tolist() for e in embeddings]

                print('Job {} out of {} done for {} - {} x 1 vector embedding'.format(index + 1, totaljobs, i,
                                                                                      len(job_embeddings)))
                embeddings_list.append(job_embeddings)

            df['bert_embeddings'] = embeddings_list

            df.to_csv(self.output_filepath.format(filename_base),index=False)
