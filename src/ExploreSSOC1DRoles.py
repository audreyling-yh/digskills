import helper
import pandas as pd
import seaborn as sns

class ExploreSSOC1DRoles:
    def __init__(self, ict_jobs_filepath, img_data_filepath):
        self.ict_jobs_filepath = ict_jobs_filepath
        self.img_data_filepath = img_data_filepath

        self.jobs = None

    def run(self):
        self.jobs = helper.get_all_postings()

        ict_jobs = pd.read_csv(self.ict_jobs_filepath)
        self.indicate_digital_roles(ict_jobs)

        self.count_year_roles()
        ssoc1d_year_count = self.count_ssoc_roles()
        ssoc1d_year_dig_count = self.count_dig_roles()
        self.prop_dig_roles(ssoc1d_year_count, ssoc1d_year_dig_count)
        self.explore_ssic_within_ssoc(ssoc1d=2)

    def indicate_digital_roles(self, ict_jobs):
        # indicate which MCF job posting is for a digital job
        dig_ssoc4d = ict_jobs['ssoc4d'].unique()
        self.jobs['Type of job'] = self.jobs['ssoc4d'].apply(lambda x: 'ICT' if x in dig_ssoc4d else 'Non-ICT')

    def count_year_roles(self):
        # count the number of total job postings per year
        df = self.jobs.groupby(['year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'year_count'}, inplace=True)

        df = helper.scale_counts(df, 'year_count')
        print(df['scaled_year_count'].sum())

        helper.save_csv(df, self.img_data_filepath.format('count_postings_by_year'))

    def count_ssoc_roles(self):
        # count the number of total job postings per year
        df = self.jobs.groupby(['SSOC1D', 'year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'ssoc1d_year_count'}, inplace=True)

        df = helper.scale_counts(df, 'ssoc1d_year_count')

        helper.save_csv(df, self.img_data_filepath.format('count_postings_by_ssoc1d_year'))
        return df

    def count_dig_roles(self):
        # How many digital roles are there in each SSOC1D per year?
        df = self.jobs.groupby(['SSOC1D', 'year', 'Type of job'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'ssoc1d_year_dig_count'}, inplace=True)
        df = helper.scale_counts(df, 'ssoc1d_year_dig_count')
        helper.save_csv(df, self.img_data_filepath.format('count_dig_roles_by_ssoc1d_year'))

        helper.lineplot(df=df,
                        x_col='year',
                        y_col='scaled_ssoc1d_year_dig_count',
                        x_label='Year',
                        y_label='Number of MCF job postings',
                        title='Total number of jobs by SSOC1D',
                        img_name='SSOC1D_dig_role_count',
                        hue_col='SSOC1D',
                        style_col='Type of job',
                        legendloc='right',
                        palette='dark:salmon_r'
                        )

        return df

    def prop_dig_roles(self, ssoc1d_year_count, ssoc1d_year_dig_count):
        # Proportion of digital roles within each SSOC1D per year
        df = ssoc1d_year_count.merge(ssoc1d_year_dig_count, on=['SSOC1D', 'year'])
        df['ssoc1d_year_prop'] = df['ssoc1d_year_dig_count'] / df['ssoc1d_year_count']
        df = df[df['Type of job'] == 'ICT']
        helper.save_csv(df, self.img_data_filepath.format('prop_dig_roles_by_ssoc1d_year'))

        helper.lineplot(df=df,
                        x_col='year',
                        y_col='ssoc1d_year_prop',
                        x_label='Year',
                        y_label='Proportion',
                        title='Proportion of ICT jobs within each SSOC1D',
                        img_name='SSOC1D_dig_role_prop',
                        hue_col='SSOC1D',
                        legendloc='right',
                        legendtitle='SSOC1D',
                        palette='dark:salmon_r'
                        )

    def explore_ssic_within_ssoc(self, ssoc1d=2):
        # Filter to only include postings from SSOC1D group
        df = self.jobs[self.jobs['SSOC1D'] == ssoc1d]

        # Include only ICT jobs
        df = df[df['Type of job'] == 'ICT']

        # Remove postings with invalid SSIC4D
        df['valid_ssic'] = df['ssic4d'].apply(lambda x: x.isdigit())
        df = df[df['valid_ssic']]

        # Get total number of ICT jobs annually by SSIC
        df = df.groupby(['ssic4d', 'year'])['JOB_POST_ID'].count().reset_index()
        df.rename(columns={'JOB_POST_ID': 'ssic4d_year_dig_count'}, inplace=True)
        df = helper.scale_counts(df, 'ssic4d_year_dig_count')
        helper.save_csv(df, self.img_data_filepath.format('count_ssic_dig_roles_by_year_ssoc{}').format(str(ssoc1d)))

        # Remove SSIC4Ds that don't have figures for all 4 years
        temp = df.groupby(['ssic4d'])['year'].nunique().reset_index()
        temp = temp[temp['year'] == 4]
        ssic_list = temp['ssic4d'].tolist()
        df = df[df['ssic4d'].isin(ssic_list)]

        # Get SSIC4Ds that have consistently increased digital job count from 2018 to 2020
        temp = df[df['year'].isin(['2018', '2019', '2020'])]
        temp['diff'] = temp['scaled_ssic4d_year_dig_count'].diff()
        temp = temp[temp['year'].isin(['2019', '2020'])]

        temp['bool'] = temp['diff'] > 0
        temp2 = temp.groupby(['ssic4d'])['bool'].sum().reset_index()
        temp2 = temp2[temp2['bool'] == 2]
        ssic_list = temp2['ssic4d'].tolist()
        temp2 = df[df['ssic4d'].isin(ssic_list)]
        helper.save_csv(temp2, self.img_data_filepath.format('count_increasing_ssic_dig_roles_by_year_ssoc{}').format(
            str(ssoc1d)))

        temp['bool'] = temp['diff'] > 100
        temp = temp.groupby(['ssic4d'])['bool'].sum().reset_index()
        temp = temp[temp['bool'] == 2]
        ssic_list = temp['ssic4d'].tolist()
        df = df[df['ssic4d'].isin(ssic_list)]
        helper.save_csv(df, self.img_data_filepath.format('count_top_increasing_ssic_dig_roles_by_year_ssoc{}').format(
            str(ssoc1d)))

        helper.lineplot(df=df,
                        x_col='year',
                        y_col='scaled_ssic4d_year_dig_count',
                        x_label='Year',
                        y_label='ICT job posting count',
                        title='Number of ICT jobs by SSIC4D within SSOC Group {}'.format(str(ssoc1d)),
                        img_name='SSOC{}_SSIC_dig_role_count'.format(str(ssoc1d)),
                        hue_col='ssic4d',
                        legendloc='right',
                        legendtitle='SSIC4D',
                        palette='mako'
                        )

        # Exclude recruitment agencies
        ssic_list=[x for x in ssic_list if x!='7810']
        df = df[df['ssic4d'].isin(ssic_list)]

        palette= sns.color_palette("mako", 4)[:4]

        helper.lineplot(df=df,
                        x_col='year',
                        y_col='scaled_ssic4d_year_dig_count',
                        x_label='Year',
                        y_label='ICT job posting count',
                        title='Number of ICT jobs by SSIC4D within SSOC Group {}'.format(str(ssoc1d)),
                        img_name='SSOC{}_SSIC_dig_role_count_filtered'.format(str(ssoc1d)),
                        hue_col='ssic4d',
                        legendloc='right',
                        legendtitle='SSIC4D',
                        palette=palette
                        )
