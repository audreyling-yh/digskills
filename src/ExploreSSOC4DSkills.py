import ast
import pandas as pd
import config
import helper
from collections import Counter


class ExploreSSOC4DSkills:
    def __init__(self, img_data_filepath, img_filepath):
        self.img_data_filepath = img_data_filepath
        self.img_filepath = img_filepath

        self.jobs = None

    def run(self):
        self.jobs = helper.get_all_postings()
        self.prep_jobs()

        self.get_largest_demand_increase_ssoc4d()
        self.explore_ssoc4d_tracks()
        self.explore_ssoc4d_tracks(subtracks=True)
        self.explore_ssoc4d_track_skills()
        self.explore_ssoc4d_track_skills(subtracks=True)
        self.explore_ssoc4d_postings_track()
        self.explore_ssoc4d_postings_track(subtracks=True)

    def prep_jobs(self):
        self.jobs['tracks_final'] = self.jobs['tracks_final'].apply(lambda x: ast.literal_eval(x))
        self.jobs['subtracks_final'] = self.jobs['subtracks_final'].apply(lambda x: ast.literal_eval(x))

        self.jobs['tracks_count'] = self.jobs['tracks_count'].apply(lambda x: Counter(ast.literal_eval(x)))
        self.jobs['subtracks_count'] = self.jobs['subtracks_count'].apply(lambda x: Counter(ast.literal_eval(x)))

        self.jobs['year'] = self.jobs['year'].apply(str)

        self.jobs['digital'] = (self.jobs['num_tracks_final'] + self.jobs['num_subtracks_final']) > 0

    def get_largest_demand_increase_ssoc4d(self):
        # get ssoc4ds with the largest increase in demand of jobs requiring digital skills

        # Get jobs that require digital skills
        df = self.jobs[self.jobs['digital']]

        # Get dif in num of jobs requiring dig skills from 2018 to 2021
        df = df[df['year'].isin(['2018', '2021'])]
        ssoc_year_count = df.groupby(['ssoc4d', 'year'])['digital'].sum().reset_index()
        ssoc_year_count = helper.scale_counts(ssoc_year_count, 'digital')
        ssoc_year_count.sort_values(by=['ssoc4d', 'year'], ascending=True, inplace=True)
        ssoc_year_count = ssoc_year_count[ssoc_year_count['year'] == '2021']
        ssoc_year_count['diff'] = ssoc_year_count['scaled_digital'].diff()

        # Get ten SSOCs with highest diff
        ssoc_year_count.sort_values(by=['diff'], ascending=False, inplace=True)
        helper.save_csv(ssoc_year_count, 'data/count_digskills_job_2021_2018_diff_by_ssoc4d.csv')
        ssoc4dlist = ssoc_year_count.head(10)['ssoc4d'].tolist()

        self.jobs = self.jobs[self.jobs['ssoc4d'].isin(ssoc4dlist)]

    def explore_ssoc4d_tracks(self, subtracks=False):
        # Get number of job postings (scaled) per track for top SSOC4Ds
        if subtracks:
            col = 'subtracks_final'
        else:
            col = 'tracks_final'

        df = self.jobs.explode(col)
        df = df.groupby(['ssoc4d', col, 'year'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')

        if not subtracks:
            df[col] = [config.track_mapping[x] for x in df[col]]

        helper.save_csv(df, 'data/{}_by_year_top_ssoc.csv'.format(col.split('_')[0]))

        # Rank tracks within each SSOC4D and year (highest job postings = highest demand = rank 1)
        df['rank'] = df.groupby(['ssoc4d', 'year'])['scaled_JOB_POST_ID'].rank("dense", ascending=False)

        # Get 2021-2018 diff in ranking for each track
        temp = df[df['year'].isin(['2018', '2021'])]
        temp.sort_values(by=['ssoc4d', col, 'year'], inplace=True)
        temp['rankdelta'] = temp[['rank']].diff()  # change in ranking from 2018 to 2021 (negative means rise in ranks)
        temp = temp[temp['year'] == '2021']

        # Sum up delta across all SSOC4Ds for each track
        tracks_rankdelta = temp.groupby([col])['rankdelta'].sum().reset_index()

        helper.save_csv(tracks_rankdelta, 'data/{}_rank_delta.csv'.format(col.split('_')[0]))


    def explore_ssoc4d_postings_track(self,subtracks=False):
        if subtracks:
            col = 'num_subtracks_final'
            newcol='avg_subtracks_per_posting'
        else:
            col = 'num_tracks_final'
            newcol='avg_tracks_per_posting'

        # Get avg number of tracks required per job posting per year and SSOC4D
        df=self.jobs.groupby(['ssoc4d','year'])[col].mean().reset_index()
        df.rename(columns={col: newcol}, inplace=True)
        helper.save_csv(df,'data/avg_{}_per_posting.csv'.format(col.split('_')[1]))

        # Get 2021-2018 diff in avg skills for each job posting
        temp = df[df['year'].isin(['2018', '2021'])]
        temp.sort_values(by=['ssoc4d', 'year'], inplace=True)
        temp['delta'] = temp[[newcol]].diff()
        temp = temp[temp['year'] == '2021']

        helper.save_csv(temp, 'data/avg_{}_per_posting_delta.csv'.format(col + 's'))


    def explore_ssoc4d_track_skills(self, subtracks=False):
        if subtracks:
            col = 'subtracks_count'
        else:
            col = 'tracks_count'

        # within a ssoc4d and year, get the avg. number of skills belonging to each track
        df = pd.DataFrame()

        for ssoc in self.jobs['ssoc4d'].unique():
            ssocjobs = self.jobs[self.jobs['ssoc4d'] == ssoc]

            for i in ssocjobs['year'].unique():
                temp = ssocjobs[ssocjobs['year'] == i]
                tracks_sum = dict(sum(temp[col], Counter()))
                tracks_avg = [(tracks_sum[x] / len(temp)) for x in tracks_sum.keys()]

                temp_df = pd.DataFrame(data={'ssoc4d': ssoc, 'year': i, 'track': tracks_sum.keys(),
                                             'avg_skills_required': tracks_avg})
                df = df.append(temp_df)

        if subtracks:
            df.rename(
                columns={'track': 'subtrack', 'avg_skills_required': 'avg_skills_required'},
                inplace=True)
        else:
            df['track'] = [config.track_mapping[x] for x in df['track']]

        helper.save_csv(df, 'data/avg_skills_by_{}_ssoc4d_year.csv'.format(col.split('_')[0]))

        # Get 2021-2018 diff in avg skills for each track
        if subtracks:
            col='subtrack'
        else:
            col='track'

        temp = df[df['year'].isin(['2018', '2021'])]
        temp.sort_values(by=['ssoc4d', col, 'year'], inplace=True)
        temp['delta'] = temp[['avg_skills_required']].diff()
        temp = temp[temp['year'] == '2021']

        # Get average change in avg skills for each track
        tracks_avgdelta=temp.groupby([col])['delta'].mean().sort_values().reset_index()

        helper.save_csv(tracks_avgdelta, 'data/{}_avgskills_delta.csv'.format(col+'s'))

