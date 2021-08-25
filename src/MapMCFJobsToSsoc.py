import os
import pandas as pd
import config
from datetime import datetime


class MapMCFJobsToSsoc:
    def __init__(self, postings_dir, output_filepath):
        self.postings_dir = postings_dir
        self.output_filepath = output_filepath

    def run(self):
        self.job_to_ssoc(self.postings_dir)

    def job_to_ssoc(self, folder):
        # Combine job info and detail files
        jobdetail_filepaths = [folder + x for x in os.listdir(folder) if x.startswith('JOB_POST_DETAIL')]
        jobinfo_filepaths = [config.jobposting_detail_info_mapping[x] for x in jobdetail_filepaths]

        for idx, path in enumerate(jobdetail_filepaths):
            print(path)
            detail = pd.read_csv(path, delimiter='\t', encoding="ISO-8859-1", error_bad_lines=False)
            info = pd.read_csv(jobinfo_filepaths[idx], delimiter='\t', encoding="ISO-8859-1", error_bad_lines=False)

            # check column title (2020-07 and 08 data is a bit noisy)
            bool = [True if (x.startswith('^') and x.endswith('^')) else False for x in detail.columns]
            if sum(bool) == len(bool):
                detail = detail.applymap(lambda x: str(x)[1:-1])
                detail.columns = [str(x)[1:-1] for x in detail.columns]

            # Merge job info (SSOC etc.) with job details (job description etc.)
            merged = detail.merge(info[['JOB_POST_ID', 'JOB_SSOC_CODE_6D', 'HIRE_ORG_SSIC_CODE']],
                                  on='JOB_POST_ID', how='inner')

            # Get SSOC4D and 1D
            merged['ssoc4d'] = [str(x)[:4] for x in merged['JOB_SSOC_CODE_6D']]
            merged['ssoc1d'] = [str(x)[:1] for x in merged['JOB_SSOC_CODE_6D']]

            # Drop jobs that are non-PMET (Drop SSOC1D 4-9)
            excluded = ['4', '5', '6', '7', '8', '9', 'X', 'n']
            merged_filtered = merged[~merged['ssoc1d'].isin(excluded)]
            print(len(merged) - len(merged_filtered), 'non-PMET jobs dropped')

            merged_filtered['date'] = merged_filtered['YYYYMM'].apply(lambda x: datetime.strptime(str(x), '%Y%m'))
            merged_filtered['year'] = merged_filtered['date'].apply(lambda x: x.year)
            merged_filtered['month'] = merged_filtered['date'].apply(lambda x: x.month)

            output = self.output_filepath.format(path.split('/')[-1].split('.')[0])
            merged_filtered.to_csv(output, index=False)
