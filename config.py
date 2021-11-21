filepaths = {
    'abilities': {
        'folder': 'data/',
        'filename': 'abilities.csv'
    },
    'analysis': {
        'folder': 'data/analysis/',
        'filename': '{}.csv'
    },
    'job_ability_cosine_matrix': {
        'folder': 'data/job_ability_cosine/',
        'filename': '{}_cosine.npy'
    },
    'job_tsc_cosine_matrix': {
        'folder': 'data/job_tsc_cosine/',
        'filename': '{}_cosine.npy'
    },
    'digital_jobs_dau_ssoc': {
        'folder': 'data/ict_jobs/',
        'filename': 'ict_jobs_dau_ssoc.csv'
    },
    'img': {
        'folder': 'img/',
        'filename': '{}.png'
    },
    'mcf_jobpostings_bert': {
        'folder': 'data/jobpostings_bert/',
        'filename': '{}_bert.npy'
    },
    'mcf_jobpostings_final': {
        'folder': 'data/jobpostings_final/',
        'filename': '{}_final.csv'
    },
    'mcf_jobpostings_raw': {
        'folder': 'data/jobpostings_raw/',
    },
    'mcf_jobpostings_processed': {
        'folder': 'data/jobpostings_processed/',
        'filename': '{}_processed.csv'
    },
    'programming_languages': {
        'folder': 'data/',
        'filename': 'programminglanguages.txt'
    },
    'resume_ability_cosine_matrix': {
        'folder': 'data/resume_ability_cosine/',
        'filename': '{}_cosine.npy'
    },
    'resume_tsc_cosine_matrix': {
        'folder': 'data/resume_tsc_cosine/',
        'filename': '{}_cosine.npy'
    },
    'resumes_bert': {
        'folder': 'data/resumes_bert/',
        'filename': '{}_bert.npy'
    },
    'resumes_final': {
        'folder': 'data/resumes_final/',
        'filename': '{}_final.csv'
    },
    'resumes_raw': {
        'folder': 'data/resumes_raw/',
    },
    'resumes_processed': {
        'folder': 'data/resumes_processed/',
        'filename': 'resumes_{}.csv'
    },
    'role_to_tsc': {
        'folder': 'data/ssg/',
        'filename': 'link_role_to_tsc.csv'
    },
    'ssg_ict_skills_original': {
        'folder': 'data/ssg/',
        'filename': 'ict_skills.csv'
    },
    'ssoc2015_to_2020_original': {
        'folder': 'data/ssoc/',
        'filename': 'Correspondence Tables between SSOC2020 and 2015v18.xlsx'
    },
    'ssoc_index_dau': {
        'folder': 'data/ssoc/',
        'filename': '[Long][20210830]SF-SSOCMapping.csv'
    },
}

# AES2019 SSIC2015 (Version 2018) mapping based on Wenjie's file
aes_ssic_mapping = {
    '10,32': 'Manufacturing',
    '35,38': 'Utilities',
    '41,43': 'Construction',
    '46,47': 'Wholesale & Retail Trade',
    '49,53': 'Transportation & Storage',
    '55,56': 'Accomodation & Food Services',
    '58,63': 'Information & Communications',
    '64,66': 'Finance & Insurance',
    '68,82': 'Business Services',
    '84,97': 'Other Services Industries'
}

# job description stop words (for word clouds)
my_stopwords = ['will', 'well', 'able', 'required', 'provide', 'experience', 'work', 'with', 'team', 'e', 'g',
                'working', 'looking', 'knowledge', 'ability', 'equivalent', 'closely', 'role', 'responsible',
                'player', 'hand', 'year', 'at', 'least', 'within', 'including', 'requirements', 'requirement',
                'expected', 'new', 'used', 'use', 'role', 'job', 'singapore', 'using', 'sg', 'shortlisted', 'candidate',
                'ideal', 'regret', 'inform', 'notified', 'relevant', 'prepare', 'preparing', 'skill', 'understand',
                'understanding', 'across', 'ensure', 'need', 'must', 'understands', 'years', 'good', 'command', 'of',
                'candidates', 'position', 'positions', 'responsibilities', 'responsibility']

jobposting_detail_info_mapping = {
    'data/jobpostings_raw/JOB_POST_DETAILS_1.txt': 'data/jobpostings_raw/JOB_POST.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_2.txt': 'data/jobpostings_raw/JOB_POST.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202007.txt': 'data/jobpostings_raw/JOB_POST_202007.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202008.txt': 'data/jobpostings_raw/JOB_POST_202008.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS3_202009_rectified.txt': 'data/jobpostings_raw/JOB_POST3_202009.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202010.txt': 'data/jobpostings_raw/JOB_POST_202010.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202011.txt': 'data/jobpostings_raw/JOB_POST_202011.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202012.txt': 'data/jobpostings_raw/JOB_POST_202012.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202101.txt': 'data/jobpostings_raw/JOB_POST_202101.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202102.txt': 'data/jobpostings_raw/JOB_POST_202102.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202103.txt': 'data/jobpostings_raw/JOB_POST_202103.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202104.txt': 'data/jobpostings_raw/JOB_POST_202104.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202105.txt': 'data/jobpostings_raw/JOB_POST_202105.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202106.txt': 'data/jobpostings_raw/JOB_POST_202106.txt',
    'data/jobpostings_raw/JOB_POST_DETAILS_202107.txt': 'data/jobpostings_raw/JOB_POST_202107.txt',
}
