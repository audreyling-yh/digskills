import os
import re
import helper
import pandas as pd


class ProcessResumes:
    def __init__(self, resumes_folder, output_filepath):
        self.resumes_folder = resumes_folder
        self.output_filepath = output_filepath

    def run(self):
        for i in os.listdir(self.resumes_folder):
            print(i)

            # process month's resumes
            folderpath = self.resumes_folder + i
            self.process(folderpath, i)

    def process(self, folderpath, foldername):
        totalresumes = len(os.listdir(folderpath))

        # combine month's resumes into df
        resume_list = []
        filename_list = []
        for idx, i in enumerate(os.listdir(folderpath)):
            print('Processing resume {} out of {} for {}'.format(idx + 1, totalresumes, folderpath))
            filepath = folderpath + '/' + i
            resume = helper.read_txt(filepath)

            # exclude resume if too short
            if len(resume) > 50:
                resume_list.append(resume)
                filename_list.append(i)

        df = pd.DataFrame(data={'file': filename_list, 'resume': resume_list})
        df.drop_duplicates(subset=['resume'], keep='last', inplace=True)

        # add cols
        df = self.get_programming_languages(df)
        df = self.get_month_year(df, foldername)

        # clean df
        df = self.clean_final_df(df)

        # save df
        filepath = self.output_filepath.format(foldername)
        helper.save_csv(df, filepath)

    def get_month_year(self, df, foldername):
        # add month and year
        month = foldername[-2:]
        year = foldername[:-2]

        df['month'] = month
        df['year'] = year
        df['YYYYMM'] = foldername

        return df

    def get_programming_languages(self, df):
        # get programming languages
        df['programming_languages'] = helper.extract_programming_languages(df['resume'])

        return df

    def clean_final_df(self, df):
        # remove non-unicode characters
        df['resume']=df['resume'].apply(lambda x: re.sub(r'[^\x00-\x7f]', ' ', x))

        # remove redacted info
        df['resume']=df['resume'].apply(lambda x: re.sub('X+', '', x))

        return df
