import config
import helper
import pandas as pd


class ExploreSSOC1DSkills:
    def __init__(self, img_data_filepath):
        self.img_data_filepath = img_data_filepath

        self.jobs = None

    def run(self):
        self.jobs = helper.get_all_postings()
        self.indicate_dig_skill()

        self.count_dig_skills()
        self.prop_dig_skills()
        self.explore_ssic_within_ssoc(ssoc1d=1)
        self.explore_ssic_within_ssoc(ssoc1d=2)
        self.explore_ssic_within_ssoc(ssoc1d=3)
        self.explore_ssic()

    def indicate_dig_skill(self):
        self.jobs['sum_track'] = self.jobs['num_tracks_final'] + self.jobs['num_subtracks_final']
        self.jobs['Type of skills required'] = self.jobs['sum_track'].apply(
            lambda x: 'Digital' if x > 0 else 'Non-digital')

    def count_dig_skills(self):
        # How many postings require digital skills?
        df = self.jobs.groupby(['SSOC1D', 'year', 'Type of skills required'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'ssoc1d_year_dig_count'}, inplace=True)
        df = helper.scale_counts(df, 'ssoc1d_year_dig_count')
        helper.save_csv(df, self.img_data_filepath.format('count_dig_skills_by_ssoc1d_year'))

        df = helper.scale_counts(df, 'ssoc1d_year_dig_count')

        helper.lineplot(df=df,
                        x_col='year',
                        y_col='scaled_ssoc1d_year_dig_count',
                        x_label='Year',
                        y_label='Number of MCF job postings',
                        title='Total number of job postings by skill requirements within each SSOC1D',
                        img_name='SSOC1D_dig_skill_count',
                        hue_col='SSOC1D',
                        style_col='Type of skills required',
                        legendloc='right',
                        palette='dark:salmon_r',
                        figsize=(8,4)
                        )

    def prop_dig_skills(self):
        # What proportion of each year's jobs require dig skills per SSOC1D?
        filepath = config.filepaths['img_data']['folder'] + config.filepaths['img_data']['filename'].format(
            'count_postings_by_ssoc1d_year')
        ssoc_roles = pd.read_csv(filepath)
        ssoc_roles['year']=ssoc_roles['year'].apply(str)

        df = self.jobs[self.jobs['Type of skills required'] == 'Digital']
        df = df.groupby(['SSOC1D', 'year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'ssoc1d_year_dig_count'}, inplace=True)

        df = df.merge(ssoc_roles, on=['SSOC1D', 'year'])
        df['ssoc1d_year_dig_prop'] = df['ssoc1d_year_dig_count'] / df['ssoc1d_year_count']

        helper.lineplot(df=df,
                        x_col='year',
                        y_col='ssoc1d_year_dig_prop',
                        x_label='Year',
                        y_label='Proportion',
                        title='Proportion of job postings requiring digital skills within each SSOC1D',
                        img_name='SSOC1D_dig_skill_prop',
                        hue_col='SSOC1D',
                        legendloc='right',
                        legendtitle='SSOC1D',
                        palette='dark:salmon_r'
                        )

    def explore_ssic_within_ssoc(self,ssoc1d=2):
        # Filter to only include postings from SSOC1D group
        df = self.jobs[self.jobs['SSOC1D'] == ssoc1d]

        # Include only jobs that require digital skills
        df = df[df['Type of skills required'] == 'Digital']

        # Remove postings with invalid SSIC4D
        df['valid_ssic'] = df['ssic4d'].apply(lambda x: x.isdigit())
        df = df[df['valid_ssic']]

        # Get SSICs that have at least 10,000 postings in total
        temp = df.groupby(['ssic4d'])['JOB_POST_ID'].count().reset_index()
        temp=temp[temp['JOB_POST_ID']>10000]
        ssic_list=temp['ssic4d'].tolist()

        # Get total number of jobs requiring digital skills annually by SSIC
        df = df.groupby(['ssic4d', 'year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'ssic4d_year_dig_count'}, inplace=True)
        df = helper.scale_counts(df, 'ssic4d_year_dig_count')
        helper.save_csv(df, self.img_data_filepath.format('count_ssic_dig_skills_by_year_ssoc{}').format(str(ssoc1d)))

        df=df[df['ssic4d'].isin(ssic_list)]

        helper.lineplot(df=df,
                        x_col='year',
                        y_col='scaled_ssic4d_year_dig_count',
                        x_label='Year',
                        y_label='Number of job postings requiring digital skills',
                        title='Number of job postings requiring digital skills by SSIC4D within SSOC Group {}'.format(str(ssoc1d)),
                        img_name='SSOC{}_SSIC_dig_skills_count'.format(str(ssoc1d)),
                        hue_col='ssic4d',
                        legendloc='right',
                        legendtitle='SSIC4D',
                        palette='mako'
                        )

    def explore_ssic(self):
        # Get the proportion of jobs requiring dig skills per year per ssic
        ssic_list=['7810','7020','6202','6201']

        df = self.jobs[self.jobs['ssic4d'].isin(ssic_list)]

        ssic_year_total=df.groupby(['ssic4d','year'])['JOB_POST_ID'].count().reset_index()
        ssic_year_total.rename(columns={'JOB_POST_ID':'ssic_year_count'},inplace=True)

        temp=df[df['Type of skills required']=='Digital']
        df=temp.groupby(['ssic4d','year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'ssic_dig_year_count'}, inplace=True)

        df=df.merge(ssic_year_total,on=['ssic4d','year'],how='left')
        df['ssic_dig_year_prop']=df['ssic_dig_year_count']/df['ssic_year_count']

        helper.lineplot(df=df,
                        x_col='year',
                        y_col='ssic_dig_year_prop',
                        x_label='Year',
                        y_label='Proportion',
                        title='Proportion of job postings requiring digital skills by SSIC4D',
                        img_name='SSIC_dig_skills_prop',
                        hue_col='ssic4d',
                        legendloc='right',
                        legendtitle='SSIC4D',
                        palette='mako'
                        )
