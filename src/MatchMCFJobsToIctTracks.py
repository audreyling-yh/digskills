import pandas as pd
import ast
import os
from collections import Counter


class MatchMCFJobsToIctTracks:
    def __init__(self, ict_tsc_filepath, jobpostings_ictskills_folder, job_tracks_filepath):
        self.ict_tsc_filepath = ict_tsc_filepath
        self.jobpostings_ictskills_folder = jobpostings_ictskills_folder
        self.output_filepath = job_tracks_filepath

        self.tsc = None

    def run(self):
        self.tsc = pd.read_csv(self.ict_tsc_filepath)
        self.get_job_tracks()

    def get_job_tracks(self, tsc_threshold=5):
        track_dict = self.get_tsc_track_dict()
        subtrack_dict = self.get_tsc_subtrack_dict()

        for i in os.listdir(self.jobpostings_ictskills_folder):
            filepath = self.jobpostings_ictskills_folder + i
            filename = '_'.join(i.split('_')[:5])

            df = pd.read_csv(filepath)
            df['skill_list'] = df['skill_list'].apply(lambda x: ast.literal_eval(x))

            track_list = [(sum([track_dict[x].tolist() for x in i], [])) for i in df['skill_list'].tolist()]
            subtrack_list = [(sum([subtrack_dict[x].tolist() for x in i], [])) for i in df['skill_list'].tolist()]

            # For each listed skill, map to its main/sub track
            df['tracks_raw'] = track_list
            df['subtracks_raw'] = subtrack_list

            # Get the number of required skills for each main/sub track
            df['tracks_count'] = df['tracks_raw'].apply(lambda x: Counter(x))
            df['subtracks_count'] = df['subtracks_raw'].apply(lambda x: Counter(x))

            # must have at least x tsc of a track, then we consider the track as required
            df['tracks_final'] = df['tracks_count'].apply(
                lambda x: list(set([k for k, v in x.items() if v >= tsc_threshold])))
            df['num_tracks_final'] = df['tracks_final'].apply(len)

            df['subtracks_final'] = df['subtracks_count'].apply(
                lambda x: list(set([k for k, v in x.items() if v >= tsc_threshold])))
            df['num_subtracks_final'] = df['subtracks_final'].apply(len)

            output_filepath = self.output_filepath.format(filename)
            df.to_csv(output_filepath, index=False)

    def get_tsc_track_dict(self):
        tsc_subtrack = self.tsc.groupby(['tsc_id_proficiency_level'])['track'].unique().reset_index()
        tsc_track_dict = dict(zip(tsc_subtrack.tsc_id_proficiency_level, tsc_subtrack.track))
        return tsc_track_dict

    def get_tsc_subtrack_dict(self):
        tsc_subtrack = self.tsc.groupby(['tsc_id_proficiency_level'])['subtrack'].unique().reset_index()
        tsc_subtrack_dict = dict(zip(tsc_subtrack.tsc_id_proficiency_level, tsc_subtrack.subtrack))
        return tsc_subtrack_dict
