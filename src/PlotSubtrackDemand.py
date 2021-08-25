import ast
from collections import Counter
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import config


class PlotSubtrackDemand:
    def __init__(self, jobsubtracks_folder, year_output_filepath,ssoc_year_output_filepath):
        self.jobsubtracks_folder=jobsubtracks_folder
        self.year_output_filepath=year_output_filepath
        self.ssoc_year_output_filepath=ssoc_year_output_filepath

        self.year_subtracks=pd.DataFrame()

    def run(self):
        self.get_year_ssoc_subtracks()
        self.plot_total_demand_by_year()
        self.plot_total_demand_by_ssoc_year()

    def read_csv(self,csvpath):
        df=pd.read_csv(csvpath)
        return df

    def get_year_ssoc_subtracks(self):
        for i in os.listdir(self.jobsubtracks_folder):
            ssoc=i.split('_')[2].split('.')[0].replace('ssoc','')

            filepath=self.jobsubtracks_folder+i
            ssoc_df=self.read_csv(filepath)
            ssoc_df['final_subtrack'] = ssoc_df['final_subtrack'].apply(lambda x: ast.literal_eval(x))

            for year in ssoc_df['year'].unique():
                year_df=ssoc_df[ssoc_df['year']==year]

                year_subtracks=sum(year_df['final_subtrack'].tolist(),[])
                year_subtrack_count=Counter(year_subtracks)

                temp=pd.DataFrame(data={'year':year,
                                        'subtrack':[x.capitalize() for x in year_subtrack_count.keys()],
                                        'ssoc': ssoc,
                                        'count':year_subtrack_count.values(),
                                        'prop_of_ssoc_year':[x/1000 for x in year_subtrack_count.values()],  #sample size 1000
                                        'prop_of_year': [x / 5000 for x in year_subtrack_count.values()]
                                        }
                                  )
                self.year_subtracks=self.year_subtracks.append(temp)

        self.year_subtracks['year']=self.year_subtracks['year'].apply(str)

    def plot_total_demand_by_year(self):
        df=self.year_subtracks.groupby(['subtrack','year'])['prop_of_year'].sum().reset_index()

        sns.set()

        fig, ax = plt.subplots(figsize=(12, 8))
        g=sns.lineplot(data=df, x='year', y='prop_of_year',hue='subtrack',legend='full')\
            .set_title('Demand of each digital skill subtrack by year for top 5 SSOC4Ds')

        plt.xlabel('Year')
        plt.ylabel('Proportion of jobs requiring a subtrack')

        ax.legend(title='Subtrack',loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout()

        plt.savefig(self.year_output_filepath)
        plt.close()


    def plot_total_demand_by_ssoc_year(self):
        ssoc_list=self.year_subtracks['ssoc'].unique().tolist()\

        for ssoc in ssoc_list:
            ssoc_df=self.year_subtracks[self.year_subtracks['ssoc']==ssoc]
            ssoc_df.sort_values(by=['subtrack','year'],ascending=True,inplace=True)

            sns.set()

            fig, ax = plt.subplots(figsize=(8, 6))
            g=sns.lineplot(data=ssoc_df, x='year', y='prop_of_ssoc_year',hue='subtrack',legend='full')\
                .set_title('Demand of each digital skill subtrack by year for SSOC4D {}'
                           .format(config.ssoc4d_mapping[ssoc]),wrap=True)

            plt.xlabel('Year')
            plt.ylabel('Proportion of jobs requiring a subtrack')

            ax.legend(title='Subtrack',loc='center left', bbox_to_anchor=(1, 0.5))
            plt.tight_layout()
            plt.subplots_adjust(top=0.9)

            filepath=self.ssoc_year_output_filepath.format(ssoc)
            plt.savefig(filepath)
            plt.close()


if __name__=='__main__':
    jobfolder='data/jobsubtracks/'
    year_output_filepath= '../img/year_subtracks.png'
    ssoc_year_output_filepath='img/ssoc_year_subtrack_demand/ssoc{}_year_subtracks.png'

    plotsubtrackdemand=PlotSubtrackDemand(jobfolder,year_output_filepath,ssoc_year_output_filepath)
    plotsubtrackdemand.run()