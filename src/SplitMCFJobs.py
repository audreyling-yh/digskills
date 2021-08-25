import pandas as pd
import os
import math


class SplitMCFJobs:
    def __init__(self, jobpostings_bert_folder, output_filepath):
        self.input_folder = jobpostings_bert_folder
        self.output_filepath = output_filepath

    def run(self):
        for i in os.listdir(self.input_folder):
            df = pd.read_csv(self.input_folder + i)
            self.split_file(i, df)

    def split_file(self, csvname, df):
        filename = csvname.split('.')[0]

        rows = len(df)
        maxrows = 100000

        if rows > maxrows:
            print('Splitting {}...'.format(csvname))
            num_dfs = math.ceil(rows / maxrows)

            from_row = 0
            to_row = from_row + maxrows

            for i in range(num_dfs):
                if i != num_dfs - 1:
                    short_df = df.iloc[range(from_row, to_row)]
                else:
                    short_df = df.iloc[range(from_row, rows)]

                if i == 0:
                    filepath = self.output_filepath.format(filename, '')
                else:
                    filepath = self.output_filepath.format(filename, '(' + str(i) + ')')
                short_df.to_csv(filepath, index=False)

                from_row = to_row
                to_row = from_row + maxrows

        else:
            filepath = self.output_filepath.format(filename, '')
            df.to_csv(filepath, index=False)
