import ast
import helper
import config
import pandas as pd
from collections import Counter


class ExploreRolesAndSkills:
    def __init__(self,
                 ict_jobs_filepath,
                 ict_largest_ssoc_filepath,
                 nonict_largest_ssoc_filepath,
                 tracks_ict_rankdelta_filepath,
                 subtracks_ict_rankdelta_filepath,
                 tracks_nonict_rankdelta_filepath,
                 subtracks_nonict_rankdelta_filepath,
                 tracks_ict_per_posting_delta_filepath,
                 subtracks_ict_per_posting_delta_filepath,
                 tracks_nonict_per_posting_delta_filepath,
                 subtracks_nonict_per_posting_delta_filepath,
                 skills_per_track_ict_delta_filepath,
                 skills_per_subtrack_ict_delta_filepath,
                 skills_per_track_nonict_delta_filepath,
                 skills_per_subtrack_nonict_delta_filepath
                 ):
        self.ict_jobs_filepath = ict_jobs_filepath
        self.ict_largest_ssoc_filepath = ict_largest_ssoc_filepath
        self.nonict_largest_ssoc_filepath = nonict_largest_ssoc_filepath
        self.tracks_ict_rankdelta_filepath=tracks_ict_rankdelta_filepath
        self.subtracks_ict_rankdelta_filepath=subtracks_ict_rankdelta_filepath
        self.tracks_nonict_rankdelta_filepath=tracks_nonict_rankdelta_filepath
        self.subtracks_nonict_rankdelta_filepath=subtracks_nonict_rankdelta_filepath
        self.tracks_ict_per_posting_delta_filepath=tracks_ict_per_posting_delta_filepath
        self.subtracks_ict_per_posting_delta_filepath=subtracks_ict_per_posting_delta_filepath
        self.tracks_nonict_per_posting_delta_filepath=tracks_nonict_per_posting_delta_filepath
        self.subtracks_nonict_per_posting_delta_filepath=subtracks_nonict_per_posting_delta_filepath
        self.skills_per_track_ict_delta_filepath=skills_per_track_ict_delta_filepath
        self.skills_per_subtrack_ict_delta_filepath=skills_per_subtrack_ict_delta_filepath
        self.skills_per_track_nonict_delta_filepath=skills_per_track_nonict_delta_filepath
        self.skills_per_subtrack_nonict_delta_filepath=skills_per_subtrack_nonict_delta_filepath

        self.jobs = None

    def run(self):
        self.jobs = helper.get_all_postings()
        self.prep_df()
        ict_jobs = pd.read_csv(self.ict_jobs_filepath)
        self.indicate_digital_roles(ict_jobs)

        self.explore_job()
        self.explore_job(ict=True)
        self.explore_ssoc4d_tracks(ict=False,subtracks=False)
        self.explore_ssoc4d_tracks(ict=True,subtracks=False)
        self.explore_ssoc4d_tracks(ict=False,subtracks=True)
        self.explore_ssoc4d_tracks(ict=True,subtracks=True)
        self.explore_ssoc4d_postings_track(ict=False,subtracks=False)
        self.explore_ssoc4d_postings_track(ict=True,subtracks=False)
        self.explore_ssoc4d_postings_track(ict=False,subtracks=True)
        self.explore_ssoc4d_postings_track(ict=True,subtracks=True)
        self.explore_ssoc4d_track_skills(ict=False,subtracks=False)
        self.explore_ssoc4d_track_skills(ict=True,subtracks=False)
        self.explore_ssoc4d_track_skills(ict=False,subtracks=True)
        self.explore_ssoc4d_track_skills(ict=True,subtracks=True)

    def prep_df(self):
        self.jobs['tracks_final']=self.jobs['tracks_final'].apply(lambda x: ast.literal_eval(x))
        self.jobs['subtracks_final'] = self.jobs['subtracks_final'].apply(lambda x: ast.literal_eval(x))
        self.jobs['tracks_count']=self.jobs['tracks_count'].apply(lambda x: Counter(ast.literal_eval(x)))
        self.jobs['subtracks_count'] = self.jobs['subtracks_count'].apply(lambda x: Counter(ast.literal_eval(x)))

    def indicate_digital_roles(self, ict_jobs):
        # indicate which MCF job posting is for a digital job
        dig_ssoc4d = ict_jobs['ssoc4d'].unique()
        self.jobs['Type of job'] = self.jobs['ssoc4d'].apply(lambda x: 'ICT' if x in dig_ssoc4d else 'Non-ICT')

    def explore_job(self, ict=False):
        if ict:
            df = self.jobs[self.jobs['Type of job'] == 'ICT']
            filepath = self.ict_largest_ssoc_filepath
        else:
            df = self.jobs[self.jobs['Type of job'] == 'Non-ICT']
            filepath = self.nonict_largest_ssoc_filepath

        # Get jobs that require digital skills
        df['digital'] = (df['num_tracks_final'] + df['num_subtracks_final']) > 0
        df = df[df['digital']]

        # Get number of job postings requiring digital skills for each ssoc4d
        temp = df.groupby(['ssoc4d', 'year'])['JOB_POST_ID'].count().reset_index()
        temp = helper.scale_counts(temp, 'JOB_POST_ID')

        # Get 2021-2018 difference
        temp.sort_values(by=['ssoc4d', 'year'], inplace=True)
        temp = temp[temp['year'].isin(['2018', '2021'])]
        temp['diff'] = temp['scaled_JOB_POST_ID'].diff()
        temp = temp[temp['year'] == '2021']
        temp.sort_values(by=['diff'], ascending=False, inplace=True)
        helper.save_csv(temp, filepath)

    def explore_ssoc4d_tracks(self, ict=False, subtracks=False):
        # Get number of job postings (scaled) per track for top SSOC4Ds
        if subtracks:
            col = 'subtracks_final'
            if ict:
                df = self.jobs[self.jobs['Type of job'] == 'ICT']
                delta_filepath = self.subtracks_ict_rankdelta_filepath
            else:
                df = self.jobs[self.jobs['Type of job'] == 'Non-ICT']
                delta_filepath=self.subtracks_nonict_rankdelta_filepath
        else:
            col = 'tracks_final'
            if ict:
                df = self.jobs[self.jobs['Type of job'] == 'ICT']
                delta_filepath=self.tracks_ict_rankdelta_filepath
            else:
                df = self.jobs[self.jobs['Type of job'] == 'Non-ICT']
                delta_filepath =self.tracks_nonict_rankdelta_filepath

        df = df.explode(col)
        df = df.groupby(['ssoc4d', col, 'year'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')

        if not subtracks:
            df[col] = [config.track_mapping[x] for x in df[col]]

        # Rank tracks within each SSOC4D and year (highest job postings = highest demand = rank 1)
        df['rank'] = df.groupby(['ssoc4d', 'year'])['scaled_JOB_POST_ID'].rank("dense", ascending=False)

        # Get 2021-2018 diff in ranking for each track
        temp = df[df['year'].isin(['2018', '2021'])]
        temp.sort_values(by=['ssoc4d', col, 'year'], inplace=True)
        temp['rankdelta'] = temp[['rank']].diff()  # change in ranking from 2018 to 2021 (negative means rise in ranks)
        temp = temp[temp['year'] == '2021']

        # Sum up delta across all SSOC4Ds for each track
        tracks_rankdelta = temp.groupby([col])['rankdelta'].sum().reset_index()

        helper.save_csv(tracks_rankdelta, delta_filepath)

    def explore_ssoc4d_postings_track(self, ict=False,subtracks=False):
        # diversification
        if subtracks:
            col = 'num_subtracks_final'
            newcol = 'avg_subtracks_per_posting'
            if ict:
                df = self.jobs[self.jobs['Type of job'] == 'ICT']
                delta_filepath = self.subtracks_ict_per_posting_delta_filepath
            else:
                df = self.jobs[self.jobs['Type of job'] == 'Non-ICT']
                delta_filepath=self.subtracks_nonict_per_posting_delta_filepath
        else:
            col = 'num_tracks_final'
            newcol = 'avg_tracks_per_posting'
            if ict:
                df = self.jobs[self.jobs['Type of job'] == 'ICT']
                delta_filepath = self.tracks_ict_per_posting_delta_filepath
            else:
                df = self.jobs[self.jobs['Type of job'] == 'Non-ICT']
                delta_filepath = self.tracks_nonict_per_posting_delta_filepath

        # Get avg number of tracks required per job posting per year and SSOC4D
        df = df.groupby(['ssoc4d', 'year'])[col].mean().reset_index()
        df.rename(columns={col: newcol}, inplace=True)

        # Get 2021-2018 diff in avg skills for each job posting
        temp = df[df['year'].isin(['2018', '2021'])]
        temp.sort_values(by=['ssoc4d', 'year'], inplace=True)
        temp['delta'] = temp[[newcol]].diff()
        temp = temp[temp['year'] == '2021']

        helper.save_csv(temp, delta_filepath)

    def explore_ssoc4d_track_skills(self, ict=False,subtracks=False):
        # proficiency
        if subtracks:
            col = 'subtracks_count'
            if ict:
                df = self.jobs[self.jobs['Type of job'] == 'ICT']
                delta_filepath=self.skills_per_subtrack_ict_delta_filepath
            else:
                df = self.jobs[self.jobs['Type of job'] == 'Non-ICT']
                delta_filepath=self.skills_per_subtrack_nonict_delta_filepath
        else:
            col = 'tracks_count'
            if ict:
                df = self.jobs[self.jobs['Type of job'] == 'ICT']
                delta_filepath=self.skills_per_track_ict_delta_filepath
            else:
                df = self.jobs[self.jobs['Type of job'] == 'Non-ICT']
                delta_filepath=self.skills_per_track_nonict_delta_filepath

        # within a ssoc4d and year, get the avg. number of skills belonging to each track
        deltadf = pd.DataFrame()

        for ssoc in df['ssoc4d'].unique():
            ssocjobs = df[df['ssoc4d'] == ssoc]

            for i in ssocjobs['year'].unique():
                temp = ssocjobs[ssocjobs['year'] == i]
                tracks_sum = dict(sum(temp[col], Counter()))
                tracks_avg = [(tracks_sum[x] / len(temp)) for x in tracks_sum.keys()]

                temp_df = pd.DataFrame(data={'ssoc4d': ssoc, 'year': i, 'track': tracks_sum.keys(),
                                             'avg_skills_required': tracks_avg})
                deltadf = deltadf.append(temp_df)

        # Get 2021-2018 diff in avg skills for each track
        temp = deltadf[deltadf['year'].isin(['2018', '2021'])]
        temp.sort_values(by=['ssoc4d', 'track', 'year'], inplace=True)
        temp['delta'] = temp[['avg_skills_required']].diff()
        temp = temp[temp['year'] == '2021']

        # Get average change in avg skills for each track
        tracks_avgdelta = temp.groupby(['track'])['delta'].mean().sort_values().reset_index()

        helper.save_csv(tracks_avgdelta, delta_filepath)
