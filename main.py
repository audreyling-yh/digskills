import os
import config
import sys

from src.CalculateJobAbilityCosine import CalculateJobAbilityCosine
from src.CalculateJobTscCosine import CalculateJobTscCosine
from src.ConvertAbilitiesToBert import ConvertAbilitiesToBert
from src.ConvertMCFJobsToBert import ConvertMCFJobsToBert
from src.AnalyseExtensiveMargin import AnalyseExtensiveMargin
from src.AnalyseIntensiveMargin import AnalyseIntensiveMargin
from src.ProcessICTJobs import ProcessICTJobs
from src.ProcessMCFJobs import ProcessMCFJobs
from src.MatchTscToJob import MatchTscToJob

# Create folders
filepaths = config.filepaths
folders = list(set([filepaths[k]['folder'] for k in filepaths.keys()]))
for i in folders:
    os.makedirs(i, exist_ok=True)

# Get filepaths
original_ict_skills = filepaths['ssg_ict_skills_original']['folder'] + filepaths['ssg_ict_skills_original']['filename']
original_role_to_tsc = filepaths['role_to_tsc']['folder'] + filepaths['role_to_tsc']['filename']
original_ssoc2015_to_2020 = filepaths['ssoc2015_to_2020_original']['folder'] + filepaths['ssoc2015_to_2020_original'][
    'filename']

dau_ssoc_index = filepaths['ssoc_index_dau']['folder'] + filepaths['ssoc_index_dau']['filename']

abilities = filepaths['abilities']['folder'] + filepaths['abilities']['filename']

img = filepaths['img']['folder'] + filepaths['img']['filename']

ict_jobs_with_dau_ssoc = filepaths['digital_jobs_dau_ssoc']['folder'] + filepaths['digital_jobs_dau_ssoc']['filename']

mcf_jobpostings_processed = filepaths['mcf_jobpostings_processed']['folder'] + filepaths['mcf_jobpostings_processed'][
    'filename']
mcf_jobpostings_bert = filepaths['mcf_jobpostings_bert']['folder'] + filepaths['mcf_jobpostings_bert']['filename']
mcf_jobpostings_final = filepaths['mcf_jobpostings_final']['folder'] + filepaths['mcf_jobpostings_final']['filename']

job_ability_cosine = filepaths['job_ability_cosine_matrix']['folder'] + filepaths['job_ability_cosine_matrix'][
    'filename']
job_tsc_cosine = filepaths['job_tsc_cosine_matrix']['folder'] + filepaths['job_tsc_cosine_matrix']['filename']

analysis = filepaths['analysis']['folder'] + filepaths['analysis']['filename']

# Get folders
mcf_jobpostings_raw_folder = filepaths['mcf_jobpostings_original']['folder']
mcf_jobpostings_processed_folder = filepaths['mcf_jobpostings_processed']['folder']
mcf_jobpostings_bert_folder = filepaths['mcf_jobpostings_bert']['folder']

if __name__ == '__main__':
    def process_frameworks():
        # convert ict tsc-proficiency abilities to bert word embeddings
        ca = ConvertAbilitiesToBert(original_ict_skills, abilities)
        ca.run()

        # tag each ict job with an ssoc4d 2020 (dau mapping)
        mi = ProcessICTJobs(original_role_to_tsc, dau_ssoc_index, ict_jobs_with_dau_ssoc)
        mi.run()


    def process_jobpostings():
        # tag each job posting with ssoc4d (2020) and AES sector of the hiring org, and remove non-PMET jobs
        mm = ProcessMCFJobs(mcf_jobpostings_raw_folder, mcf_jobpostings_processed, original_ssoc2015_to_2020)
        mm.run()

        # combine all job description text files into a dataframe and obtain bert embeddings for each job
        # CAUTION: Will take about 6 hours to run on GPU
        cm = ConvertMCFJobsToBert(mcf_jobpostings_processed_folder, mcf_jobpostings_bert)
        cm.run()


    def match():
        # get cosine similarity between each job and ability
        cj = CalculateJobAbilityCosine(abilities, mcf_jobpostings_bert_folder, job_ability_cosine)
        cj.run()

        # get cosine similarity between each job and tsc
        cj = CalculateJobTscCosine(abilities, original_ict_skills, mcf_jobpostings_bert_folder, job_ability_cosine,
                                   job_tsc_cosine)
        cj.run()

        # get tscs matched to each job
        mt = MatchTscToJob(original_ict_skills, mcf_jobpostings_processed_folder, job_tsc_cosine, mcf_jobpostings_final,
                           cosine_threshold=0.3)
        mt.run()


    def analyse():
        # Extensive margin
        ae = AnalyseExtensiveMargin(analysis, ict_jobs_with_dau_ssoc)
        ae.run()

        # Intensive margin
        ai = AnalyseIntensiveMargin(img, analysis, ict_jobs_with_dau_ssoc)
        ai.run()


    processes_map = {
        'PROCESS_FW': process_frameworks,
        'PROCESS_JOBS': process_jobpostings,
        'MATCH': match,
        'ANALYSIS': analyse
    }

    processes = [
        'PROCESS_FW',
        'PROCESS_JOBS',
        'MATCH',
        'ANALYSIS'
    ]

    if len(sys.argv) > 1:
        processes = [x for x in sys.argv[1].split(',')]

    for i in processes:
        func = processes_map[i]
        func()
