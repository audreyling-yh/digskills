import pandas as pd


class ProcessICTJobs:
    def __init__(self, ssg_jobs_filepath, dau_ssoc_index_filepath, output_filepath):
        self.ssg_jobs_filepath = ssg_jobs_filepath
        self.dau_ssoc_index_filepath = dau_ssoc_index_filepath
        self.output_filepath = output_filepath

    def run(self):
        ssg_jobs = pd.read_csv(self.ssg_jobs_filepath)
        dau_ssoc = pd.read_csv(self.dau_ssoc_index_filepath)

        ict = self.get_ict_jobs(ssg_jobs)
        df = self.map_role_to_ssoc(ict, dau_ssoc)
        df.to_csv(self.output_filepath, index=False)

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
