import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import config

class ExploreJobSsoc:
    def __init__(self, jobpostings_folder, output_filepath):
        self.jobpostings_folder=jobpostings_folder
        self.output_filepath=output_filepath

        self.jobs=pd.DataFrame()

    def run(self):
        self.get_all_jobs()
        self.clean_jobs()

        self.get_total_jobs()
        yearjobcount=self.get_total_jobs_per_year()

        # Explore SSOC4D
        ssoc4d_count=self.get_total_postings_per_ssoc4d()
        # top_ssoc4d=self.get_above_90p_postings_ssoc4d(ssoc4d_count)
        top_ssoc4d=self.get_top_postings_ssoc4d(ssoc4d_count,num=5)

        top_ssoc4d_count=self.get_total_postings_for_top_ssoc4ds(top_ssoc4d)
        top_ssoc4d_prop=self.get_prop_postings_for_top_ssoc4ds(top_ssoc4d, yearjobcount)

        self.plot_top_ssoc4d_total_jobs_per_year(top_ssoc4d_count)
        self.plot_top_ssoc4d_prop_jobs_per_year(top_ssoc4d_prop)

        # Explore SSOC1D
        ssoc1d_count=self.get_total_postings_per_ssoc1d()
        ssoc1d_prop=self.get_prop_postings_per_ssoc1d(ssoc1d_count,yearjobcount)

        self.plot_ssoc1d_total_jobs_per_year(ssoc1d_count)
        self.plot_ssoc1d_prop_jobs_per_year(ssoc1d_prop)


    def get_all_jobs(self):
        for i in os.listdir(self.jobpostings_folder):
            filepath=self.jobpostings_folder+i
            temp = pd.read_csv(filepath)
            self.jobs = self.jobs.append(temp, ignore_index=True)
        self.jobs.drop_duplicates(inplace=True)

    def clean_jobs(self):
        self.jobs['ssoc4d'] = self.jobs['ssoc4d'].apply(lambda x: '{:<04s}'.format(str(x)))
        self.jobs['ssoc1d'] = self.jobs['ssoc4d'].apply(lambda x: x[0])
        self.jobs['bool'] = self.jobs['ssoc4d'].apply(
            lambda x: True if x not in ['X100', 'X200'] else False)  # unusable occupation classifications
        self.jobs = self.jobs[self.jobs['bool']].drop(columns=['bool'])

    def get_total_jobs(self):
        print(len(self.jobs))

    def get_total_jobs_per_year(self):
        yearjobcount = self.jobs.groupby(['year'])['JOB_POST_ID'].count().reset_index()
        yearjobcount.rename(columns={'JOB_POST_ID': 'total_year_jobs'}, inplace=True)
        return yearjobcount


    def get_total_postings_per_ssoc4d(self):
        ssoc4d_count=self.jobs.groupby(['ssoc4d'])['JOB_POST_ID'].count().reset_index()
        ssoc4d_count.sort_values(by=['JOB_POST_ID'],ascending=False,inplace=True)
        ssoc4d_count.rename(columns={'JOB_POST_ID':'ssoc4d_total_jobs'},inplace=True)
        return ssoc4d_count

    def get_above_90p_postings_ssoc4d(self, ssoc4d_count):
        # get ssoc4ds whose postings count > 90th percentile
        p90=np.percentile(ssoc4d_count['ssoc4d_total_jobs'],95)
        top_ssoc4d=ssoc4d_count[ssoc4d_count['ssoc4d_total_jobs']>p90]
        ssoc4dlist=top_ssoc4d['ssoc4d'].tolist()

        self.jobs['bool']=self.jobs['ssoc4d'].apply(lambda x: True if x in ssoc4dlist else False)
        top_ssoc4d=self.jobs[self.jobs['bool']]
        self.jobs.drop(columns=['bool'],inplace=True)

        top_ssoc4d['ssoc4d_name']=[config.ssoc4d_mapping[x] if x in config.ssoc4d_mapping.keys() else x for x in top_ssoc4d['ssoc4d']]

        return top_ssoc4d

    def get_top_postings_ssoc4d(self, ssoc4d_count, num=10):
        # get x ssoc4ds with the most postings
        top_ssoc4d=ssoc4d_count.head(num)
        ssoc4dlist=top_ssoc4d['ssoc4d'].tolist()

        self.jobs['bool']=self.jobs['ssoc4d'].apply(lambda x: True if x in ssoc4dlist else False)
        top_ssoc4d=self.jobs[self.jobs['bool']]
        self.jobs.drop(columns=['bool'],inplace=True)

        top_ssoc4d['ssoc4d_name']=[config.ssoc4d_mapping[x] for x in top_ssoc4d['ssoc4d']]

        return top_ssoc4d

    def get_total_postings_for_top_ssoc4ds(self, top_ssoc4d):
        top_ssoc4d_count=top_ssoc4d.groupby(['ssoc4d','ssoc4d_name','year'])['JOB_POST_ID'].count().reset_index()
        top_ssoc4d_count.rename(columns={'JOB_POST_ID':'ssoc4d_total_year_jobs'},inplace=True)
        return top_ssoc4d_count

    def get_prop_postings_for_top_ssoc4ds(self, top_ssoc4d, yearjobcount):
        top_ssoc4d_prop=top_ssoc4d.groupby(['ssoc4d','ssoc4d_name','year'])['JOB_POST_ID'].count().reset_index()
        top_ssoc4d_prop.rename(columns={'JOB_POST_ID':'ssoc4d_total_year_jobs'},inplace=True)

        top_ssoc4d_prop=top_ssoc4d_prop.merge(yearjobcount,on='year',how='left')
        top_ssoc4d_prop['prop']=top_ssoc4d_prop['ssoc4d_total_year_jobs']/top_ssoc4d_prop['total_year_jobs']

        print(top_ssoc4d_prop.groupby('year')['prop'].sum())

        return top_ssoc4d_prop

    def plot_top_ssoc4d_prop_jobs_per_year(self, ssoc4d_prop):
        ssoc4d_prop['ssoc1d']=ssoc4d_prop['ssoc4d'].apply(lambda x: x[:1])
        ssoc4d_prop['year']=ssoc4d_prop['year'].apply(str)

        sns.set()

        # 1 for all ssoc4d
        fig, ax = plt.subplots(figsize=(8, 8))

        g = sns.lineplot(data=ssoc4d_prop, x='year', y='prop', hue='ssoc4d_name', legend='full', palette='Set2').\
            set_title('Proportion of job postings each year by SSOC4D')

        plt.ylabel('Proportion of total job postings per year')
        plt.xlabel('Year')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),borderaxespad=0.)
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.tight_layout()

        filepath = self.output_filepath.format('ssoc4d_prop_jobs')
        plt.savefig(filepath)
        plt.close()

        # 1 for each ssoc1d's ssoc4d
        # for i in ssoc4d_prop['ssoc1d'].unique():
        #     temp=ssoc4d_prop[ssoc4d_prop['ssoc1d']==i]
        #
        #     fig, ax = plt.subplots(figsize=(8, 8))
        #
        #     g=sns.lineplot(data=temp,x='year',y='prop',hue='ssoc4d')\
        #         .set_title('Proportion of job postings each year by Major Group {}: {}'.format(i, config.ssoc_group[i]))
        #
        #     plt.ylim(0,0.1)
        #     plt.ylabel('Proportion of total job postings per year')
        #     plt.xlabel('Year')
        #
        #     filepath=self.output_filepath.format('ssoc4d_{}_prop_jobs').format(i)
        #     plt.savefig(filepath)
        #     plt.close()

    def plot_top_ssoc4d_total_jobs_per_year(self, ssoc4d_count):
        ssoc4d_count['ssoc1d']=ssoc4d_count['ssoc4d'].apply(lambda x: x[:1])
        ssoc4d_count['year']=ssoc4d_count['year'].apply(str)

        sns.set()

        # 1 for all ssoc4d
        fig, ax = plt.subplots(figsize=(8, 8))

        g = sns.lineplot(data=ssoc4d_count, x='year', y='ssoc4d_total_year_jobs', hue='ssoc4d_name', legend='full',
                         palette='Set2').set_title('Total job postings each year by SSOC4D')

        plt.ylabel('Total job postings per year')
        plt.xlabel('Year')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),borderaxespad=0.)
        # plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.tight_layout()

        filepath = self.output_filepath.format('ssoc4d_total_jobs')
        plt.savefig(filepath)
        plt.close()

        # 1 for each ssoc1d's ssoc4d
        # for i in ssoc4d_count['ssoc1d'].unique():
        #     temp=ssoc4d_count[ssoc4d_count['ssoc1d']==i]
        #
        #     fig, ax = plt.subplots(figsize=(8, 8))
        #
        #     g=sns.lineplot(data=temp,x='year',y='ssoc4d_total_year_jobs',hue='ssoc4d')\
        #         .set_title('Total job postings each year by Major Group {}: {}'.format(i, config.ssoc_group[i]))
        #
        #     plt.ylabel('Total job postings per year')
        #     plt.xlabel('Year')
        #
        #     filepath=self.output_filepath.format('ssoc4d_{}_total_jobs').format(i)
        #     plt.savefig(filepath)
        #     plt.close()

    def get_total_postings_per_ssoc1d(self):
        ssoc1d_count=self.jobs.groupby(['ssoc1d','year'])['JOB_POST_ID'].count().reset_index()
        ssoc1d_count.rename(columns={'JOB_POST_ID':'ssoc1d_total_year_jobs'},inplace=True)

        for i in ['n','X']:
            ssoc1d_count=ssoc1d_count[ssoc1d_count['ssoc1d']!=i]

        ssoc1d_count['ssoc1d_name']=[config.ssoc_group[x] for x in ssoc1d_count['ssoc1d']]

        return ssoc1d_count

    def get_prop_postings_per_ssoc1d(self, ssoc1d_count, yearjobcount):
        ssoc1d_prop=ssoc1d_count.merge(yearjobcount[['year','total_year_jobs']],on='year',how='left')
        ssoc1d_prop['prop']=ssoc1d_prop['ssoc1d_total_year_jobs']/ssoc1d_prop['total_year_jobs']
        return ssoc1d_prop

    def plot_ssoc1d_total_jobs_per_year(self,ssoc1d_count):
        ssoc1d_count['year']=ssoc1d_count['year'].apply(str)

        sns.set()
        fig, ax = plt.subplots(figsize=(12, 8))

        g=sns.lineplot(data=ssoc1d_count,x='year',y='ssoc1d_total_year_jobs',hue='ssoc1d_name')

        g.set_title('Total job postings each year by SSOC1D')
        plt.ylabel('Total job postings per year')
        plt.xlabel('Year')
        plt.legend(title='SSOC1D', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.tight_layout()

        filepath=self.output_filepath.format('ssoc1d_total_jobs')
        plt.savefig(filepath)
        plt.close()

    def plot_ssoc1d_prop_jobs_per_year(self,ssoc1d_prop):
        ssoc1d_prop['year']=ssoc1d_prop['year'].apply(str)

        sns.set()
        fig, ax = plt.subplots(figsize=(12, 8))

        g=sns.lineplot(data=ssoc1d_prop,x='year',y='prop',hue='ssoc1d_name')

        g.set_title('Proportion of job postings each year by SSOC1D')
        plt.ylabel('Proportion of job postings per year')
        plt.xlabel('Year')
        plt.legend(title='SSOC1D', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.tight_layout()

        filepath=self.output_filepath.format('ssoc1d_prop_jobs')
        plt.savefig(filepath)
        plt.close()


if __name__=='__main__':
    postings_folder='data/jobpostings_ssoc/'
    image_filepath='img/ssoc_postings/{}.png'

    #TODO: os create directory if not exists

    explorejobssoc=ExploreJobSsoc(postings_folder,image_filepath)
    explorejobssoc.run()








