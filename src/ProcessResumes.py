import os
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
            self.process(folderpath)

    def process(self, folderpath):
        totalresumes = len(os.listdir(folderpath))

        # combine month's resumes into df
        resume_list = []
        filename_list = []
        for idx, i in enumerate(os.listdir(folderpath)):
            print('Processing resume {} out of {} for {}'.format(idx+1, totalresumes, folderpath))
            filepath = folderpath + '/' + i
            resume = helper.read_txt(filepath)

            # exclude resume if too short
            if len(resume) > 50:
                resume_list.append(resume)
                filename_list.append(i)

        df = pd.DataFrame(data={'file': filename_list, 'resume': resume_list})
        df.drop_duplicates(subset=['resume'], keep='first', inplace=True)

        # get programming languages
        df['programming_languages'] = helper.extract_programming_languages(df['resume'])

        # save df
        month = folderpath.replace(self.resumes_folder, '')
        filepath = self.output_filepath.format(month)
        helper.save_csv(df, filepath)
