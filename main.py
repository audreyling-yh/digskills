import os
import config
import helper
import sys


# Create folders
filepaths = config.filepaths
folders = list(set([filepaths[k]['folder'] for k in filepaths.keys()]))
for i in folders:
    os.makedirs(i, exist_ok=True)

# Get folders
ssg_ictroles_docx_folder = filepaths['ssg_ict_roles_docx']['folder']
ssg_icttscs_docx_folder = filepaths['ssg_ict_tscs_docx']['folder']

mcf_raw_folder = filepaths['mcf_raw']['folder']
mcf_processed_folder = filepaths['mcf_processed']['folder']
mcf_bert_folder = filepaths['mcf_bert']['folder']

# Get filepaths
# frameworks
nonict_dig_tscs = helper.get_filepath('ssg_nonict_dig_tscs')
apps_tools = helper.get_filepath('ssg_appstools')
sfw = helper.get_filepath('ssg_sfw')
frameworks = helper.get_filepath('frameworks')
ict_roles = helper.get_filepath('frameworks').format('ict_roles', 'csv')
ict_tscs = helper.get_filepath('frameworks').format('ict_tscs', 'csv')
abilities = helper.get_filepath('frameworks').format('ict_tsc_abilities', 'csv')
ict_roles_bert = helper.get_filepath('frameworks').format('ict_roles', 'npy')
abilities_bert = helper.get_filepath('frameworks').format('ict_tsc_abilities', 'npy')
sfw_ssoc_mapping = helper.get_filepath('sfw_ssoc_mapping')
ssoc2010_2020_mapping = helper.get_filepath('ssoc2010_2020_mapping')

# mcf
mcf_raw = helper.get_filepath('mcf_raw')
mcf_processed = helper.get_filepath('mcf_processed')
mcf_bert = helper.get_filepath('mcf_bert')

# original_ict_skills = helper.get_filepath('ssg_ict_skills_original')
# original_role_to_tsc = helper.get_filepath('role_to_tsc')
# original_ssoc2015_to_2020 = helper.get_filepath('ssoc2015_to_2020_original')
#
# dau_ssoc_index = helper.get_filepath('ssoc_index_dau')
# ssoc_index = helper.get_filepath('ssoc_index_dos')
#
# ict_jobs_with_ssoc = helper.get_filepath('digital_jobs_ssoc')

# mcf_jobpostings_final = helper.get_filepath('mcf_jobpostings_final')

# job_ability_cosine = helper.get_filepath('job_ability_cosine_matrix')
# job_tsc_cosine = helper.get_filepath('job_tsc_cosine_matrix')

# analysis = helper.get_filepath('analysis')
# img = helper.get_filepath('img')


if __name__ == '__main__':
    def process_frameworks():
        from src.ExtractICTRoles import ExtractICTRoles
        from src.ProcessICTJobs import ProcessICTJobs
        from src.ExtractICTSkills import ExtractICTSkills
        from src.ConvertICTRolesToBert import ConvertICTRolesToBert
        from src.ConvertAbilitiesToBert import ConvertAbilitiesToBert
        from src.Convert2010To2020SSOC import Convert2010To2020SSOC

        # extract ICT roles from framework
        ei = ExtractICTRoles(ssg_ictroles_docx_folder, ict_roles)
        ei.run()

        # tag each ICT role with an ssoc
        mi = ProcessICTJobs(ict_roles, sfw_ssoc_mapping)
        mi.run()

        # extract ICT skills (TSCs) with knowledge and abilities from framework
        ei = ExtractICTSkills(ssg_icttscs_docx_folder, ict_tscs, nonict_dig_tscs, sfw)
        ei.run()

        # convert ict roles to bert embeddings
        ci = ConvertICTRolesToBert(ict_roles, ict_roles_bert)
        ci.run()

        # convert ict tsc-proficiency abilities to bert word embeddings
        ca = ConvertAbilitiesToBert(ict_tscs, abilities, abilities_bert)
        ca.run()

        # get mapping from DOS SSOC 2010 to SSOC 2020
        c2 = Convert2010To2020SSOC(frameworks, ssoc2010_2020_mapping)
        c2.run()


    def process():
        from src.ProcessMCFJobs import ProcessMCFJobs
        from src.ConvertMCFJobsToBert import ConvertMCFJobsToBert

        # tag each job posting with SSOC 2020, AES, apps & tools, and remove non-PMET jobs
        mm = ProcessMCFJobs(mcf_raw_folder, mcf_raw, mcf_processed_folder, mcf_processed, ssoc2010_2020_mapping,
                            apps_tools, ict_roles, overwrite=False)
        mm.run()

        # convert each month's job postings to bert embeddings
        # CAUTION: Will take about xxx hours to run on GPU
        cm = ConvertMCFJobsToBert(mcf_processed_folder, mcf_bert_folder, mcf_bert, overwrite=False)
        cm.run()


    # def match():
        # from src.CalculateJobAbilityCosine import CalculateJobAbilityCosine
        # from src.CalculateJobTscCosine import CalculateJobTscCosine
        # from src.MatchTscToJob import MatchTscToJob

    #     # get cosine similarity between each job and ability
    #     cj = CalculateJobAbilityCosine(abilities, mcf_jobpostings_bert_folder, job_ability_cosine)
    #     cj.run()
    #
    #     # get cosine similarity between each job and tsc
    #     cj = CalculateJobTscCosine(abilities, original_ict_skills, mcf_jobpostings_bert_folder, job_ability_cosine,
    #                                job_tsc_cosine)
    #     cj.run()
    #
    #     # get tscs matched to each job
    #     mt = MatchTscToJob(original_ict_skills, mcf_jobpostings_processed_folder, job_tsc_cosine, mcf_jobpostings_final,
    #                        cosine_threshold=0.4)
    #     mt.run()
    #
    #     # get cosine similarity between each resume and ability
    #     cj = CalculateJobAbilityCosine(abilities, resumes_bert_folder, resume_ability_cosine)
    #     cj.run()
    #
    #     # get cosine similarity between each resume and tsc
    #     cj = CalculateJobTscCosine(abilities, original_ict_skills, resumes_bert_folder, resume_ability_cosine,
    #                                resume_tsc_cosine)
    #     cj.run()
    #
    #     # get tscs matched to each resume
    #     mt = MatchTscToJob(original_ict_skills, resumes_processed_folder, resume_tsc_cosine, resumes_final,
    #                        cosine_threshold=0.4)
    #     mt.run()
    #
    #
    # def analyse():
        # from src.AnalyseGap import AnalyseGap
        # from src.AnalyseExtensiveMargin import AnalyseExtensiveMargin
        # from src.AnalyseIntensiveMargin import AnalyseIntensiveMargin
    #     # Extensive margin (demand)
    #     ae = AnalyseExtensiveMargin(analysis, ict_jobs_with_ssoc)
    #     ae.run()
    #
    #     # Intensive margin (demand)
    #     ai = AnalyseIntensiveMargin(img, analysis, ict_jobs_with_ssoc)
    #     ai.run()
    #
    #     # analyse tsc gap
    #     ag = AnalyseGap(analysis)
    #     ag.run()


    processes_map = {
        'PROCESS_FW': process_frameworks,
        'PROCESS': process,
        # 'MATCH': match,
        # 'ANALYSIS': analyse
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
