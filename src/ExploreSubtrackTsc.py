import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class ExploreSubtrackTsc:
    def __init__(self, ict_tsc_filepath, ict_tsc_filtered_filepath, img_output_filepath):
        self.ict_filepath = ict_tsc_filepath
        self.ict_tsc_filtered_filepath = ict_tsc_filtered_filepath
        self.img_filepath = img_output_filepath

        self.ict = None

    def run(self):
        self.ict = self.read_csv(self.ict_filepath)
        self.clean_ict()

        self.get_total_tsc_prof()
        self.get_total_track_count()

        # Analyse TSC-proficiencies
        tsc_track_count = self.get_tsc_track_count()
        self.plot_tsc_track_count(tsc_track_count, subtrack=True)
        self.plot_tsc_track_count(tsc_track_count, subtrack=False)
        self.drop_tsc_with_many_tracks(tsc_track_count, track_threshold=2, subtrack_threshold=5)
        self.get_total_track_count()

        # Analyse subtracks
        track_tsc_count = self.get_track_tsc_count(subtrack=False)
        subtrack_tsc_count = self.get_track_tsc_count(subtrack=True)
        self.plot_track_tsc_count(track_tsc_count, subtrack=False)
        self.plot_track_tsc_count(subtrack_tsc_count, subtrack=True)

    def read_csv(self, csvpath):
        df = pd.read_csv(csvpath)
        return df

    def clean_ict(self):
        self.ict['subtrack'] = self.ict['subtrack'].apply(lambda x: x.split(','))
        self.ict = self.ict.explode('subtrack')

    def get_total_tsc_prof(self):
        # we have 244 unique TSC-proficiency
        # some tsc-proficiencies appear in more than 1 subtrack
        print(self.ict['tsc_id_proficiency_level'].nunique(), 'TSC-proficiencies')

    def get_total_track_count(self):
        print(len(set(self.ict['track'])), 'unique tracks')
        print(len(set(self.ict['subtrack'])), 'unique subtracks')

    def get_tsc_track_count(self):
        # Get number of unique tracks per TSC-prof
        track = pd.pivot_table(self.ict, index='tsc_id_proficiency_level', values=['track'],
                               aggfunc=[lambda x: list(set(x)), 'nunique']).reset_index()
        track.columns = track.columns.droplevel(1)
        track.rename(columns={'<lambda>': 'track_list', 'nunique': 'track_count'}, inplace=True)

        # Get number of unique subtracks per TSC-prof
        subtrack = pd.pivot_table(self.ict, index='tsc_id_proficiency_level', values=['subtrack'],
                                  aggfunc=[lambda x: list(set(x)), 'nunique']).reset_index()
        subtrack.columns = subtrack.columns.droplevel(1)
        subtrack.rename(columns={'<lambda>': 'subtrack_list', 'nunique': 'subtrack_count'}, inplace=True)

        # Merge both
        tsc_track_count = track.merge(subtrack, on=['tsc_id_proficiency_level'])

        return tsc_track_count

    def plot_tsc_track_count(self, df, subtrack=False):
        sns.set()
        if subtrack:
            sns.histplot(df, x='subtrack_count', bins=26)
            plt.title('Number of sub-tracks a skill belongs to')
            plt.xlabel('Number of sub-tracks')
            file = self.img_filepath.format('tsc_subtrack_count')
        else:
            sns.histplot(df, x='track_count', color='#F88300', bins=6)
            plt.title('Number of main tracks a skill belongs to')
            plt.xlabel('Number of main tracks')
            file = self.img_filepath.format('tsc_track_count')

        plt.ylabel('Number of skills')
        plt.savefig(file)
        plt.close()

    def drop_tsc_with_many_tracks(self, df, track_threshold=3, subtrack_threshold=4):
        # Drop TSC-profs that have too many tracks and subtracks
        df = df[df['track_count'] <= track_threshold]
        df = df[df['subtrack_count'] <= subtrack_threshold]
        tscidprof_list = df['tsc_id_proficiency_level'].tolist()
        self.ict = self.ict[self.ict['tsc_id_proficiency_level'].isin(tscidprof_list)]

        self.save_csv(self.ict, self.ict_tsc_filtered_filepath)
        print('{} TSC-proficiencies left'.format(len(tscidprof_list)))

    def get_track_tsc_count(self, subtrack=False):
        if subtrack:
            track = self.ict.groupby(['subtrack'])['tsc_id_proficiency_level'].nunique().reset_index()
        else:
            track = self.ict.groupby(['track'])['tsc_id_proficiency_level'].nunique().reset_index()

        track.sort_values(by=['tsc_id_proficiency_level'], ascending=False, inplace=True)

        print(track.head(6))

        return track

    def plot_track_tsc_count(self, df, subtrack=False):
        sns.set()
        if subtrack:
            sns.histplot(df, x='tsc_id_proficiency_level', bins=20)
            plt.title('Number of skills belonging to a sub-track')
            plt.ylabel('Number of sub-tracks')
            file = self.img_filepath.format('subtrack_tsc_count')
        else:
            sns.histplot(df, x='tsc_id_proficiency_level', bins=6, color='#F88300')
            plt.title('Number of skills belonging to a main track')
            plt.ylabel('Number of main tracks')
            file = self.img_filepath.format('track_tsc_count')

        plt.xlabel('Number of skills')
        plt.savefig(file)
        plt.close()

    def save_csv(self, df, filepath):
        df.to_csv(filepath, index=False)
