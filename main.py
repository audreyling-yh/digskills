import os
import config
import helper
import sys

from src.CalculateJobAbilityCosine import CalculateJobAbilityCosine
from src.CalculateJobTscCosine import CalculateJobTscCosine
from src.ConvertAbilitiesToBert import ConvertAbilitiesToBert
from src.ConvertMCFJobsToBert import ConvertMCFJobsToBert
from src.ConvertResumesToBert import ConvertResumesToBert
from src.AnalyseExtensiveMargin import AnalyseExtensiveMargin
from src.AnalyseIntensiveMargin import AnalyseIntensiveMargin
from src.MatchTscToJob import MatchTscToJob
from src.ProcessICTJobs import ProcessICTJobs
from src.ProcessMCFJobs import ProcessMCFJobs
from src.ProcessResumes import ProcessResumes

# Create folders
filepaths = config.filepaths
folders = list(set([filepaths[k]['folder'] for k in filepaths.keys()]))
for i in folders:
    os.makedirs(i, exist_ok=True)

# Get filepaths
original_ict_skills = helper.get_filepath('ssg_ict_skills_original')
original_role_to_tsc = helper.get_filepath('role_to_tsc')
original_ssoc2015_to_2020 = helper.get_filepath('ssoc2015_to_2020_original')

dau_ssoc_index = helper.get_filepath('ssoc_index_dau')

abilities = helper.get_filepath('abilities')
ict_jobs_with_dau_ssoc = helper.get_filepath('digital_jobs_dau_ssoc')

mcf_jobpostings_processed = helper.get_filepath('mcf_jobpostings_processed')
mcf_jobpostings_bert = helper.get_filepath('mcf_jobpostings_bert')
mcf_jobpostings_final = helper.get_filepath('mcf_jobpostings_final')

resumes_processed = helper.get_filepath('resumes_processed')
resumes_bert = helper.get_filepath('resumes_bert')
resumes_final = helper.get_filepath('resumes_final')

job_ability_cosine = helper.get_filepath('job_ability_cosine_matrix')
job_tsc_cosine = helper.get_filepath('job_tsc_cosine_matrix')
resume_ability_cosine = helper.get_filepath('resume_ability_cosine_matrix')
resume_tsc_cosine = helper.get_filepath('resume_tsc_cosine_matrix')

analysis = helper.get_filepath('analysis')
img = helper.get_filepath('img')

# Get folders
mcf_jobpostings_raw_folder = filepaths['mcf_jobpostings_raw']['folder']
mcf_jobpostings_processed_folder = filepaths['mcf_jobpostings_processed']['folder']
mcf_jobpostings_bert_folder = filepaths['mcf_jobpostings_bert']['folder']
resumes_raw_folder = filepaths['resumes_raw']['folder']
resumes_processed_folder = filepaths['resumes_processed']['folder']
resumes_bert_folder = filepaths['resumes_bert']['folder']

if __name__ == '__main__':
    def process_frameworks():
        # convert ict tsc-proficiency abilities to bert word embeddings
        ca = ConvertAbilitiesToBert(original_ict_skills, abilities)
        ca.run()

        # tag each ict job with an ssoc4d 2020 (dau mapping)
        mi = ProcessICTJobs(original_role_to_tsc, dau_ssoc_index, ict_jobs_with_dau_ssoc)
        mi.run()


    def process():
        # # tag each job posting with ssoc4d (2020) and AES sector of the hiring org, and remove non-PMET jobs
        # mm = ProcessMCFJobs(mcf_jobpostings_raw_folder, mcf_jobpostings_processed, original_ssoc2015_to_2020)
        # mm.run()
        #
        # # combine all job description text files into a dataframe and obtain bert embeddings for each job
        # # CAUTION: Will take about 8 hours to run on GPU
        # cm = ConvertMCFJobsToBert(mcf_jobpostings_processed_folder, mcf_jobpostings_bert)
        # cm.run()

        # clean resumes
        pr = ProcessResumes(resumes_raw_folder, resumes_processed)
        pr.run()

        # combine all resume text files into a dataframe and obtain bert embeddings for each resume
        cr = ConvertResumesToBert(resumes_processed_folder, resumes_bert)
        cr.run()


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
                           cosine_threshold=0.4)
        mt.run()

        # get cosine similarity between each resume and ability
        cj = CalculateJobAbilityCosine(abilities, resumes_bert_folder, resume_ability_cosine)
        cj.run()

        # get cosine similarity between each resume and tsc
        cj = CalculateJobTscCosine(abilities, original_ict_skills, resumes_bert_folder, resume_ability_cosine,
                                   resume_tsc_cosine)
        cj.run()

        # get tscs matched to each resume
        mt = MatchTscToJob(original_ict_skills, resumes_processed_folder, resume_tsc_cosine, resumes_final,
                           cosine_threshold=0.4)
        mt.run()


    def analyse():
        # Extensive margin (demand)
        ae = AnalyseExtensiveMargin(analysis, ict_jobs_with_dau_ssoc)
        ae.run()

        # Intensive margin (demand)
        ai = AnalyseIntensiveMargin(img, analysis, ict_jobs_with_dau_ssoc)
        ai.run()


    processes_map = {
        'PROCESS_FW': process_frameworks,
        'PROCESS': process,
        'MATCH': match,
        'ANALYSIS': analyse
    }

    processes = [
        'PROCESS_FW',
        'PROCESS',
        'MATCH',
        'ANALYSIS'
    ]

    if len(sys.argv) > 1:
        processes = [x for x in sys.argv[1].split(',')]

    for i in processes:
        func = processes_map[i]
        func()
