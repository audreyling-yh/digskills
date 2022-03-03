filepaths = {
    'ssoc2010_2020_mapping': {
        'folder':'data/frameworks/',
        'filename': 'ssoc2010to2020mapping.csv'
    },
    'sfw_ssoc_mapping': {
        'folder': 'data/frameworks/DOS/',
        'filename': 'SSOC2020 Alphabetical Index.xlsx'
    },
    'frameworks': {
        'folder': 'data/frameworks/',
        'filename': '{}.{}'
    },
    'ssg_nonict_dig_tscs': {
        'folder': 'data/frameworks/SSG/',
        'filename': 'Digital TSCs (non-ICT sector).xlsx'
    },
    'ssg_appstools': {
        'folder': 'data/frameworks/SSG/',
        'filename': 'finalAppsTools (20220223).xlsx'
    },
    'ssg_sfw': {
        'folder': 'data/frameworks/SSG/',
        'filename': 'sfw_dataset-2022-01-06.xlsx'
    },
    'ssg_ict_roles_docx': {
        'folder': 'data/frameworks/SSG/SFw ICT/SFw_ICT_Skills Map_Top_5_GSC/'
    },
    'ssg_ict_tscs_docx': {
        'folder': 'data/frameworks/SSG/SFw ICT/SFw ICT TSCs V2.1/'
    },
    'mcf_raw': {
        'folder':'data/mcf/raw/',
        'filename': '{}/{}'
    },
    'mcf_processed': {
        'folder': 'data/mcf/processed/',
        'filename': '{}.hdf5'
    },
    'mcf_bert': {
        'folder': 'data/mcf/bert/',
        'filename': '{}.npy',
    },

    # 'analysis': {
    #     'folder': 'data/analysis/',
    #     'filename': '{}.csv'
    # },
    # 'job_ability_cosine_matrix': {
    #     'folder': 'data/job_ability_cosine/',
    #     'filename': '{}_cosine.npy'
    # },
    # 'job_tsc_cosine_matrix': {
    #     'folder': 'data/job_tsc_cosine/',
    #     'filename': '{}_cosine.npy'
    # },

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
