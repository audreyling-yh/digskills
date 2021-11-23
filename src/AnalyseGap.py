import helper
import pandas as pd
from collections import Counter


class AnalyseGap:
    def __init__(self, analysis_filepath):
        self.analysis_filepath = analysis_filepath

        self.postings = pd.DataFrame()
        self.resumes = pd.DataFrame()

    def run(self):
        self.read_data()

        # rank tscs (without proficiency level) by demand and supply
        tsc_demand = self.rank_tsc(self.postings)
        filepath = self.analysis_filepath.format('1q21_tsc_demand')
        helper.save_csv(tsc_demand, filepath)

        tsc_supply = self.rank_tsc(self.resumes)
        filepath = self.analysis_filepath.format('1q21_tsc_supply')
        helper.save_csv(tsc_supply, filepath)

        # rank tscs (with proficiency level) by demand and supply
        tsc_prof_demand = self.rank_tsc_prof(self.postings)
        filepath = self.analysis_filepath.format('1q21_tscprof_demand')
        helper.save_csv(tsc_prof_demand, filepath)

        tsc_prof_supply = self.rank_tsc_prof(self.resumes)
        filepath = self.analysis_filepath.format('1q21_tscprof_supply')
        helper.save_csv(tsc_prof_supply, filepath)

        # rank programming languages by demand and supply
        pl_demand = self.rank_programming_skills(self.postings)
        filepath = self.analysis_filepath.format('1q21_pl_demand')
        helper.save_csv(pl_demand, filepath)

        pl_supply = self.rank_programming_skills(self.resumes)
        filepath = self.analysis_filepath.format('1q21_pl_supply')
        helper.save_csv(pl_supply, filepath)

    def read_data(self):
        self.postings = helper.get_1q21_data(resumes=False)
        self.resumes = helper.get_1q21_data(resumes=True)

    def rank_aes_postings(self):
        self.postings.groubpy(['AES'])

    def rank_tsc(self, df):
        # drop rows without tsc
        df = df[df['tsc_count'] > 0]

        # rank tscs (ignore tsc level) by absolute count in df
        df = df.explode('tsc_list')
        df['tsc'] = df['tsc_list'].apply(lambda x: x[0])
        tscs_count = dict(Counter(df['tsc']))
        tscs_df = pd.DataFrame(data={'tsc': tscs_count.keys(), 'count': tscs_count.values()})
        tscs_df.sort_values(by=['count'], ascending=False, inplace=True)

        return tscs_df

    def rank_tsc_prof(self, df):
        # drop rows without tsc
        df = df[df['tsc_count'] > 0]

        # rank tscs (with tsc level) by absolute count in df
        df = df.explode('tsc_list')
        df['tsc'] = df['tsc_list'].apply(lambda x: x[0])
        tscs_count = dict(Counter(df['tsc_list']))
        tscs_map = {k:k[0] for k in tscs_count.keys()}
        tscs_df = pd.DataFrame(data={'tsc_proficiency': tscs_count.keys(), 'count': tscs_count.values()})
        tscs_df['tsc']=tscs_df['tsc_proficiency'].apply(lambda x: tscs_map[x])
        tscs_df.sort_values(by=['count'], ascending=False, inplace=True)

        return tscs_df

    def rank_programming_skills(self, df):
        # drop rows without programming languages
        df['pl_count'] = df['programming_languages'].apply(len)
        df = df[df['pl_count'] > 0]

        # rank programming skills by absolute count in df
        df = df.explode('programming_languages')
        pl_count = dict(Counter(df['programming_languages']))
        pl_df = pd.DataFrame(data={'programming_language': pl_count.keys(), 'count': pl_count.values()})
        pl_df.sort_values(by=['count'], ascending=False, inplace=True)

        return pl_df
