import ast
import pandas as pd
import networkx as nx
import helper
import matplotlib.pyplot as plt

class ExploreSSOC4DSkills:
    def __init__(self, img_data_filepath, img_filepath):
        self.img_data_filepath=img_data_filepath
        self.img_filepath=img_filepath

        self.jobs=None

    def run(self):
        self.jobs=helper.get_all_postings()
        self.prep_jobs()

        self.get_largest_ssoc4d()

        self.explore_ssoc4d_tracks(ssoc1d=1)
        self.explore_ssoc4d_tracks(ssoc1d=2)
        self.explore_ssoc4d_tracks(ssoc1d=3)

        self.explore_ssoc4d_subtracks(ssoc1d=1)
        self.explore_ssoc4d_subtracks(ssoc1d=2)
        self.explore_ssoc4d_subtracks(ssoc1d=3)

    def prep_jobs(self):
        self.jobs['tracks_final']=self.jobs['tracks_final'].apply(lambda x: ast.literal_eval(x))
        self.jobs['subtracks_final']=self.jobs['subtracks_final'].apply(lambda x: ast.literal_eval(x))

    def get_largest_ssoc4d(self):
        df=self.jobs.groupby(['SSOC1D','ssoc4d'])['JOB_POST_ID'].count().reset_index()
        df=df.sort_values(by=['JOB_POST_ID'],ascending=False)

        largest=pd.DataFrame()
        for i in df['SSOC1D'].unique():
            temp2=df[df['SSOC1D']==i]
            temp2=temp2.head(5)
            largest=largest.append(temp2)
        largest.to_csv(self.img_data_filepath.format('ssoc4d_top_postings_count'))

        ssoc_list=largest['ssoc4d']
        self.jobs=self.jobs[self.jobs['ssoc4d'].isin(ssoc_list)]

    def explore_ssoc4d_tracks(self, ssoc1d=1):
        df=self.jobs[self.jobs['SSOC1D']==ssoc1d]
        df=df.explode('tracks_final')

        track_mapping={
            'professional services':'strategy',
            'data':'data',
            'security':'cybersecurity',
            'software and applications':'software',
            'infrastructure':'infrastructure',
            'support':'support'
        }
        df=df.groupby(['ssoc4d','tracks_final','year'])['JOB_POST_ID'].count().reset_index()
        df=helper.scale_counts(df,'JOB_POST_ID')
        df['tracks_final']=[track_mapping[x] for x in df['tracks_final']]
        helper.save_csv(df,self.img_data_filepath.format('tracks_by_year_top_ssoc{}'.format(str(ssoc1d))))

        for i in df['year'].unique():
            temp=df[df['year']==i]

            fig,ax=plt.subplots(figsize=(10, 10))
            ax.set_title('SSOC4D Main Track Mapping for {}'.format(i))

            # plot bipartite graph
            B = nx.Graph()
            B.add_nodes_from(temp['ssoc4d'], bipartite=0)
            B.add_nodes_from(temp['tracks_final'], bipartite=1)
            B.add_weighted_edges_from(
                [(row['ssoc4d'], row['tracks_final'], row['scaled_JOB_POST_ID']/900) for idx, row in temp.iterrows()],
                weight='weight')

            # Update position for node from each group
            pos = {}
            l, r = nx.bipartite.sets(B)
            pos.update((node, (1, index)) for index, node in enumerate(l))
            pos.update((node, (1.5, index)) for index, node in enumerate(r))

            color_dict = {0: '#fcb103', 1: '#036ffc'}
            color_list = [color_dict[i[1]] for i in B.nodes.data('bipartite')]
            nx.draw_networkx_nodes(B,
                                   pos,
                                   node_size=[v[1]*300 for v in B.degree],
                                   node_color=color_list
                                   )

            weights = list(nx.get_edge_attributes(B, 'weight').values())
            nx.draw_networkx_edges(B,
                                   pos,
                                   width=weights,
                                   alpha=0.6
                                   )

            nx.draw_networkx_labels(B, pos=pos,font_size=10)

            ax.axis("off")
            plt.savefig(self.img_filepath.format('SSOC{}_track_bipartite_{}'.format(str(ssoc1d),str(i))))
            plt.close()


    def explore_ssoc4d_subtracks(self,ssoc1d=1):
        df = self.jobs[self.jobs['SSOC1D'] == ssoc1d]
        df = df.explode('subtracks_final')

        df = df.groupby(['ssoc4d', 'subtracks_final', 'year'])['JOB_POST_ID'].count().reset_index()
        df = helper.scale_counts(df, 'JOB_POST_ID')
        helper.save_csv(df,self.img_data_filepath.format('subtracks_by_year_top_ssoc{}'.format(str(ssoc1d))))
