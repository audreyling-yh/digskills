import pandas as pd
import config

"""
This class filters the SSG Skills Framework TSC list to include
only the TSC-proficiencies that are required by at least 1 job
under the ICT Skills Framework.
"""


class GetIctSkills:
    def __init__(self, tsc_items_filepath, ict_jobs_filepath, output_filepath):
        self.tsc_filepath = tsc_items_filepath
        self.ict_filepath = ict_jobs_filepath
        self.output_filepath = output_filepath

    def run(self):
        tsc = pd.read_csv(self.tsc_filepath)
        ict = pd.read_csv(self.ict_filepath)
        icttsc = self.get_ict_tsc(tsc, ict)
        icttsc.to_csv(self.output_filepath, index=False)

    def get_ict_tsc(self, tsc_df, ict_df):
        # Exclude CEO and CTO from job roles
        ict_df = ict_df[~ict_df['track'].str.contains('/')]

        # Add sub-tracks
        ict_df['subtrack'] = [','.join(config.job_subtrack[row['track']][row['job_role']])
                              if row['job_role'] in config.job_subtrack[row['track']].keys() else ''
                              for idx, row in ict_df.iterrows()]

        # Drop job roles that cannot be matched to a sub-track
        ict_df = ict_df[ict_df['subtrack'] != '']

        # Get abilities list for each ICT TSC
        ict_tsc = ict_df.merge(tsc_df[[x for x in tsc_df.columns if x not in ['sector', 'tsc_category']]],
                               on=['tsc_id', 'tsc_title', 'proficiency_level'],
                               how='left'
                               )

        ict_tsc['tsc_id_proficiency_level'] = list(zip(ict_tsc.tsc_id, ict_tsc.proficiency_level))
        ict_tsc = ict_tsc[['tsc_id',
                           'track',
                           'subtrack',
                           'tsc_title',
                           'proficiency_level',
                           'proficiency_description',
                           'knowledge_list',
                           'knowledge_id',
                           'abilities_list',
                           'abilities_id',
                           'tsc_id_proficiency_level',
                           'bert_embeddings'
                           ]].drop_duplicates()

        # Note that each TSC-prof might fall under dif tracks and sub tracks and hence form multiple rows

        return ict_tsc
