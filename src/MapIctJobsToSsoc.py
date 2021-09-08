import pandas as pd


class MapIctJobsToSsoc:
    def __init__(self, ict_jobs_filepath, ssoc_index_filepath, dau_ssoc_index_filepath, output_filepath):
        self.ict_jobs_filepath = ict_jobs_filepath
        self.ssoc_index_filepath = ssoc_index_filepath
        self.dau_ssoc_index_filepath = dau_ssoc_index_filepath
        self.output_filepath = output_filepath

    def run(self):
        ict = pd.read_csv(self.ict_jobs_filepath)
        dau_ssoc = pd.read_csv(self.dau_ssoc_index_filepath)

        print(ict.columns)
        print(dau_ssoc.columns)

        ict = self.get_ict_jobs(ict)
        df = self.map_role_to_ssoc(ict, dau_ssoc)
        # df.to_csv(self.output_filepath, index=False)

        #### FOR MAPPING TO ORIGINAL SSOC2020 INDEX (NOT IN USE)
        # ssoc=pd.read_excel(self.ssoc_index_filepath,skiprows=6,header=1)
        # ict_jobs=self.get_ict_jobs(ict)
        # ssg_ssoc=self.clean_ssoc(ssoc)
        # self.ict_to_ssoc(ict_jobs,ssg_ssoc)

    def get_ict_jobs(self, df):
        # Filter all SSG jobs to only ICT ones
        df = df[df['sector'] == 'infocomm technology']

        # Filter out sales track
        df = df[df['track'] != 'sales and marketing']

        # Get clean job name
        df['job_role'] = df['job_role'].apply(lambda x: '/'.join([i.strip() for i in x.split('/')]) if '/' in x else x)

        return df

    def map_role_to_ssoc(self, ict, dau_ssoc):
        # Get ssoc1d from ssoc4d
        dau_ssoc['SSOC4DMapping'] = dau_ssoc['SSOC4DMapping'].astype(str)
        dau_ssoc['SSOC1D'] = dau_ssoc['SSOC4DMapping'].apply(lambda x: x[0])

        # All 102 job roles will be mapped
        # Each ICT role is mapped to 1 ssoc4d (by coincidence; the dau mapping can be one role to many SSOC)
        df = ict.merge(dau_ssoc[['role_id', 'job_role', 'SSOC4DMapping', 'SSOC1D']], on=['role_id', 'job_role'],
                       how='left')

        # Drop not-purely-ICT SSOC4Ds
        excluded_ssocs = ['1221',  # Sales and business dev managers
                          '2411',  # accountants
                          '2433',  # specialised goods sales professionals
                          '1323',  # construction managers
                          '2431'  # advertising and markerting professionals
                          ]
        df = df[~df['SSOC4DMapping'].isin(excluded_ssocs)]

        return df

    #### FOR MAPPING TO ORIGINAL SSOC2020 INDEX (NOT IN USE)
    # def clean_ssoc(self, df):
    #     # Filter to include only SSOCs in SSG framework
    #     df=df[df["Singapore Skills Framework's Job Roles*"]=='x']
    #
    #     # Filter to include only SSOCs of ICT jobs
    #     df['ict']=df['SSOC 2020 Alphabetical Index Description'].apply(lambda x: True if '(SFw-Infocomm Technology)' in x else False)
    #     df=df[df['ict']]
    #
    #     # Filter to exclude sales track
    #     df['ict'] = df['SSOC 2020 Alphabetical Index Description'].apply(lambda x: True if '(Sales and Marketing)' not in x else False)
    #     df = df[df['ict']]
    #
    #     # Get SSOC4D and SSOC1D
    #     df['ssoc4d']=df['SSOC 2020'].apply(lambda x: str(x)[:4])
    #     df['ssoc1d']=df['SSOC 2020'].apply(lambda x: str(x)[:1])
    #
    #     # Get clean job name
    #     df['job_role']=df['SSOC 2020 Alphabetical Index Description'].apply(lambda x: x.split('(')[0].lower().strip())
    #     df['job_role']=df['job_role'].apply(lambda x: x.replace('/',' / '))
    #     df.drop(columns=['ict'],inplace=True)
    #
    #     return df
    #
    # def ict_to_ssoc(self,ict_jobs, ssoc):
    #     ssoc_3cols=ssoc[['SSOC 2020','ssoc4d','ssoc1d','job_role']]
    #
    #     # Project manager has no valid SSOC mapping; drop it from df
    #     ict_ssoc=ict_jobs.merge(ssoc_3cols,on='job_role',how='inner')
    #
    #     ict_ssoc.to_csv(self.output_filepath,index=False)
