filepaths={
    'analyse_largest_demand_increase_ssoc':{
        'folder':'data/analysis/',
        'filename': 'count_digskills_job_2021_2018_diff_by_ssoc4d.csv'
    },
    'analyse_ssoc_tracks':{
        'folder':'data/analysis/',
        'filename': 'count_postings_by_tracks_year_top_ssoc.csv'
    },
    'analyse_ssoc_subtracks': {
        'folder': 'data/analysis/',
        'filename': 'count_postings_by_subtracks_year_top_ssoc.csv'
    },
    'analyse_tracks_rank_delta':{
        'folder':'data/analysis/',
        'filename': 'tracks_rank_delta.csv'
    },
    'analyse_subtracks_rank_delta':{
        'folder':'data/analysis/',
        'filename': 'subtracks_rank_delta.csv'
    },
    'analyse_tracks_diversity': {
        'folder': 'data/analysis/',
        'filename': 'avg_tracks_per_posting.csv'
    },
    'analyse_subtracks_diversity': {
        'folder': 'data/analysis/',
        'filename': 'avg_subtracks_per_posting.csv'
    },
    'analyse_tracks_diversity_delta': {
        'folder': 'data/analysis/',
        'filename': 'avg_tracks_per_posting_delta.csv'
    },
    'analyse_subtracks_diversity_delta': {
        'folder': 'data/analysis/',
        'filename': 'avg_subtracks_per_posting_delta.csv'
    },
    'analyse_tracks_proficiency': {
        'folder': 'data/analysis/',
        'filename': 'avg_skills_per_track.csv'
    },
    'analyse_subtracks_proficiency': {
        'folder': 'data/analysis/',
        'filename': 'avg_skills_per_subtrack.csv'
    },
    'analyse_tracks_proficiency_delta': {
        'folder': 'data/analysis/',
        'filename': 'avg_skills_per_track_delta.csv'
    },
    'analyse_subtracks_proficiency_delta': {
        'folder': 'data/analysis/',
        'filename': 'avg_skills_per_subtrack_delta.csv'
    },
    'cosine_matrix':{
        'folder':'data/cosine/',
        'filename':'{}_cosine.csv'
    },
    'digital_jobs_ssoc': {
        'folder': 'data/ict_jobs/',
        'filename': 'ict_jobs_ssoc.csv'
    },
    'digital_skills':{
        'folder': 'data/ict_skills/',
        'filename': 'ict_tsc.csv'
    },
    'digital_skills_filtered': {
        'folder': 'data/ict_skills/',
        'filename': 'ict_tsc_final.csv'
    },
    'img':{
        'folder':'img/',
        'filename':'{}.png'
    },
    'img_data':{
        'folder':'img/data/',
        'filename':'{}.csv',
    },
    'mcf_jobpostings_bert': {
        'folder': 'data/jobpostings_bert/',
        'filename': '{}_bert.csv'
    },
    'mcf_jobpostings_bert_split': {
        'folder': 'data/jobpostings_bert_split/',
        'filename': '{}{}.csv'
    },
    'mcf_jobpostings_original':{
        'folder': 'data/jobpostings/',
    },
    'mcf_jobpostings_ssoc':{
        'folder': 'data/jobpostings_ssoc/',
        'filename': '{}_SSOC.csv'
    },
    'mcf_jobpostings_digital_skills':{
        'folder': 'data/jobpostings_ictskills/',
        'filename': '{}_ictskills.csv'
    },
    'mcf_jobpostings_digital_tracks':{
        'folder': 'data/jobpostings_icttracks/',
        'filename': '{}_icttracks.csv'
    },
    'role_to_tsc': {
        'folder': 'data/ssg/',
        'filename': 'link_role_to_tsc.csv'
    },
    'ssg_skills_original': {
        'folder': 'data/ssg/',
        'filename': 'link_tsc_to_items.csv'
    },
    'ssg_skills_bert': {
        'folder': 'data/',
        'filename': 'link_tsc_to_items_bert.csv'
    },
    'ssoc_index_original': {
        'folder': 'data/ssoc/',
        'filename': 'SSOC2020 Alphabetical Index.xlsx'
    },

}







job_subtrack={
    'data':{
        'ai applied resesarcher': ['ai applied research'],
        'ai scientist': ['data science'],
        'ai/ml engineer':['ml engineering'],
        'associate data engineer': ['business intelligence', 'data engineering'],
        'business intelligence director':['business intelligence'],
        'business intelligence manager':['business intelligence'],
        'chief ai officer':['data engineering', 'ml engineering', 'data science', 'ai applied research'],
        'chief data officer':['data engineering', 'ml engineering', 'data science', 'ai applied research'],
        'chief data scientist': ['data science'],
        'data analyst':['business intelligence','data engineering'],
        'data architect':['data engineering'],
        'data engineer': ['data engineering'],
        'data scientist': ['data science'],
        'head of data science and ai': ['ml engineering', 'data science', 'ai applied research'],
        'information architect': ['data engineering'],
        'senior ai engineer': ['ml engineering'],
        'senior data engineer': ['data engineering'],
        'senior data scientist':['data science'],
        'senior ml engineer': ['ml engineering'],
    },
    'infrastructure':{
        'associate infrastructure engineer': ['build and maintain'],
        'associate network engineer': ['build and maintain'],
        'associate radio frequency engineer': ['build and maintain'],
        'automation and orchestration engineer': ['build and maintain'],
        'chief information officer': ['plan and design', 'build and maintain'],
        'chief technology officer': ['plan and design', 'build and maintain'],
        'cloud engineer':['build and maintain'],
        'head of infrastructure':['plan and design','build and maintain'],
        'infrastructure architect': ['plan and design'],
        'infrastructure engineer':['build and maintain'],
        'infrastructure engineering manager': ['build and maintain'],
        'infrastructure executive':['plan and design'],
        'infrastructure manager':['build and maintain'],
        'network engineer': ['build and maintain'],
        'principal cloud architect':['plan and design'],
        'principal planning and design architect':['plan and design'],
        'radio frequency engineer': ['build and maintain'],
        'senior cloud engineer':['build and maintain'],
        'senior infrastructure architect':['plan and design'],
        'senior infrastructure engineer': ['build and maintain'],
        'senior infrastructure executive': ['plan and design'],
        'senior planning and design engineer': ['build and maintain'],
        'sysops engineer': ['build and maintain'],

    },
    'software and applications': {
        'applications architect':['software engineering'],
        'applications developer':['software engineering'],
        'applications development manager':['software engineering'],
        'associate embedded systems engineer': ['embedded systems engineering'],
        'associate software engineer': ['software engineering'],
        'associate ui designer':['user interface design'],
        'chief information officer':['software engineering','embedded systems engineering','user interface design'],
        'chief technology officer': ['software engineering', 'embedded systems engineering', 'user interface design'],
        'devops engineer': ['software engineering'],
        'embedded systems architect': ['embedded systems engineering'],
        'embedded systems engineer': ['embedded systems engineering'],
        'embedded systems engineering manager': ['embedded systems engineering'],
        'head of applications development':['software engineering','embedded systems engineering','user interface design'],
        'head of product':['software engineering'],
        'head of ui/ux design':['user interface design'],
        'head of software engineering':['software engineering','embedded systems engineering','user interface design'],
        'lead ui designer':['user interface design'],
        'lead ux designer':['user interface design'],
        'platform architect':['software engineering'],
        'platform engineer':['software engineering'],
        'platform engineering manager':['software engineering'],
        'product manager':['software engineering'],
        'senior applications developer':['software engineering'],
        'senior embedded systems engineer':['embedded systems engineering'],
        'senior platform engineer':['software engineering'],
        'senior product manager':['software engineering'],
        'senior software quality assurance engineer':['software engineering'],
        'senior systems analyst':['embedded systems engineering'],
        'senior ui designer':['user interface design'],
        'senior ux designer':['user interface design'],
        'software architect':['software engineering'],
        'software engineer': ['software engineering'],
        'software engineering manager': ['software engineering'],
        'software quality assurance manager':['software engineering'],
        'software quality assurance engineer': ['software engineering'],
        'systems analysis manager':['embedded systems engineering'],
        'systems analyst':['embedded systems engineering'],
        'ui designer':['user interface design'],
        'ux designer':['user interface design']
    },
    'professional services':{ #strategy and governance
        'ai translator': ['enterprise architecture'],
        'associate business analyst':['enterprise architecture'],
        'associate ux designer':['product strategy'],
        'business analyst':['enterprise architecture'],
        'business architect':['enterprise architecture'],
        'chief technology officer':['enterprise architecture','program and project management','product strategy',
                                    'quality management','data protection','it audit'],
        'data protection executive':['data protection'],
        'data protection officer':['data protection'],
        'enterprise architect':['enterprise architecture'],
        'group data protection officer':['data protection'],
        'head of it audit':['it audit'],
        'head of it consulting':['program and project management'],
        'head of product':['product strategy'],
        'head of quality':['quality management'],
        'it auditor':['it audit'],
        'it audit manager':['it audit'],
        'it consultant':['program and project management'],
        'it consulting analyst':['program and project management'],
        'lead ux designer': ['product strategy'],
        'principal enterprise architect':['enterprise architecture'],
        'principal it consultant':['program and project management'],
        'principal solutions architect':['enterprise architecture'],
        'product manager':['product strategy'],
        'program director':['program and project management'],
        'program manager':['program and project management'],
        'project manager':['program and project management'],
        'quality assurance engineer':['quality management'],
        'quality assurance manager':['quality management'],
        'quality engineer':['quality management'],
        'quality engineering manager':['quality management'],
        'scrum master': ['program and project management'],
        'senior business analyst':['enterprise architecture'],
        'senior it consultant':['program and project management'],
        'senior product manager': ['product strategy'],
        'solutions architect': ['enterprise architecture'],
        'solutions integration architect':['enterprise architecture'],
        'ux designer':['product strategy'],
    },
    'support': { # operations and support
        'applications support engineer':['applications support'],
        'associate applications support engineer': ['applications support'],
        'associate data centre operations engineer': ['data centre and operations centre support'],
        'associate database support engineer': ['database support'],
        'associate infrastructure support engineer': ['infrastructure support'],
        'associate operations centre support engineer': ['data centre and operations centre support'],
        'associate systems support engineer': ['systems support'],
        'chief information officer': ['infrastructure support','systems support','database support',
                                      'data centre and operations centre support','applications support'],
        'data centre engineer':['data centre and operations centre support'],
        'data centre manager': ['data centre and operations centre support'],
        'data centre operations engineer': ['data centre and operations centre support'],
        'database administration manager': ['database support'],
        'database administrator': ['database support'],
        'database support engineer':['database support'],
        'head of it operations and support': ['infrastructure support','systems support','database support',
                                      'data centre and operations centre support','applications support'],
        'head of operations and support': ['infrastructure support','systems support','database support',
                                      'data centre and operations centre support','applications support'],
        'infrastructure support engineer':['infrastructure support'],
        'operations and support manager': ['infrastructure support','systems support','database support',
                                      'data centre and operations centre support','applications support'],
        'operations centre support engineer':['data centre and operations centre support'],
        'senior data centre engineer': ['data centre and operations centre support'],
        'senior database administrator':['database support'],
        'senior it operations and support manager': ['infrastructure support','systems support','database support',
                                      'data centre and operations centre support','applications support'],
        'senior systems administrator':['systems support'],
        'support analyst':['infrastructure support','systems support','database support',
                                      'data centre and operations centre support','applications support'],
        'support manager':['infrastructure support','systems support','database support',
                                      'data centre and operations centre support','applications support'],
        'systems administration manager':['systems support'],
        'systems administrator':['systems support'],
        'systems support engineer':['systems support'],
        'technical support executive': ['infrastructure support','systems support','database support',
                                      'data centre and operations centre support','applications support'],
    },
    'sales and marketing':{
        'business development manager':['sales'],
        'channel sales executive':['sales'],
        'channel sales leader':['sales'],
        'channel sales manager':['sales'],
        'customer experience manager':['customer success'],
        'customer success director':['customer success'],
        'customer success manager':['customer success'],
        'digital marketing executive':['marketing'],
        'digital marketing manager':['marketing'],
        'direct sales manager':['sales'],
        'head of marketing':['marketing'],
        'head of pre-/post-sales':['pre-sales','customer success'],
        'head of sales':['pre-sales','sales','customer success','marketing'],
        'marketing director': ['marketing'],
        'marketing executive':['marketing'],
        'marketing manager':['marketing'],
        'pre-sales consultant': ['pre-sales'],
        'pre-sales director':['pre-sales'],
        'pre-/post-sales consultant':['pre-sales','customer success'],
        'pre-/post-sales manager':['pre-sales','customer success'],
        'product marketing executive':['marketing'],
        'product marketing manager':['marketing'],
        'sales account manager':['sales'],
        'sales director':['sales'],
        'sales executive':['sales']
    },
    'security':{
        'associate security analyst':['governance risk and control',
                                              'vulnerability assessment and penetration testing','security operations',
                                              'forensics investigation','incident response','threat analysis',
                                              'security design and engineering'],
        'associate security analyst / associate security engineer':['governance risk and control',
                                              'vulnerability assessment and penetration testing','security operations',
                                              'forensics investigation','incident response','threat analysis',
                                              'security design and engineering'],
        'chief information security officer':['governance risk and control',
                                              'vulnerability assessment and penetration testing','security operations',
                                              'forensics investigation','incident response','threat analysis',
                                              'security design and engineering'],
        'cyber risk analyst':['governance risk and control'],
        'cyber risk manager':['governance risk and control'],
        'forensic investigator':['forensics investigation'],
        'forensic investigation manager': ['forensics investigation'],
        'incident investigator':['incident response'],
        'incident investigation manager': ['incident response'],
        'incident investigation manager / forensic investigation manager / threat investigation manager':[
            'incident response','forensics investigation','threat analysis'],
        'incident investigator / forensic investigator / threat investigator':['incident response',
                                                                               'forensics investigation','threat analysis'],
        'principal security engineer / principal security architect':['security design and engineering'],
        'security architect':['security design and engineering'],
        'security engineer':['security design and engineering'],
        'security executive':['security design and engineering'],
        'security operations analyst':['security operations'],
        'security operations manager': ['security operations'],
        'security penetration tester':['vulnerability assessment and penetration testing'],
        'security penetration testing manager':['vulnerability assessment and penetration testing'],
        'senior security engineer/security engineer':['security design and engineering'],
        'threat analysis manager':['threat analysis'],
        'vulnerability assessment and penetration testing analyst':['vulnerability assessment and penetration testing'],
        'vulnerability assessment and penetration testing manager': ['vulnerability assessment and penetration testing']
    },
}


jobposting_detail_info_mapping ={
    'data/jobpostings/JOB_POST_DETAILS_1.txt': 'data/jobpostings/JOB_POST.txt',
    'data/jobpostings/JOB_POST_DETAILS_2.txt': 'data/jobpostings/JOB_POST.txt',
    'data/jobpostings/JOB_POST_DETAILS_202007.txt': 'data/jobpostings/JOB_POST_202007.txt',
    'data/jobpostings/JOB_POST_DETAILS_202008.txt': 'data/jobpostings/JOB_POST_202008.txt',
    'data/jobpostings/JOB_POST_DETAILS3_202009_rectified.txt': 'data/jobpostings/JOB_POST3_202009.txt',
    'data/jobpostings/JOB_POST_DETAILS_202010.txt': 'data/jobpostings/JOB_POST_202010.txt',
    'data/jobpostings/JOB_POST_DETAILS_202011.txt': 'data/jobpostings/JOB_POST_202011.txt',
    'data/jobpostings/JOB_POST_DETAILS_202012.txt': 'data/jobpostings/JOB_POST_202012.txt',
    'data/jobpostings/JOB_POST_DETAILS_202101.txt': 'data/jobpostings/JOB_POST_202101.txt',
    'data/jobpostings/JOB_POST_DETAILS_202102.txt': 'data/jobpostings/JOB_POST_202102.txt',
    'data/jobpostings/JOB_POST_DETAILS_202103.txt': 'data/jobpostings/JOB_POST_202103.txt',
    'data/jobpostings/JOB_POST_DETAILS_202104.txt': 'data/jobpostings/JOB_POST_202104.txt',
}

ssoc_group={
    '1': 'Legislators, Senior Officials and Managers',
    '2': 'Professionals',
    '3': 'Associate Professionals and Technicians',
    '4': 'Clerical Support Workers',
    '5':'Service and Sales Workers',
    '6':'Agricultural and Fishery Workers',
    '7':'Craftsmen and Related Trades Workers',
    '8': 'Plant and Machine Operators and Assemblers',
    '9':'Cleaners, Labourers and Related Workers',
}

track_mapping = {
    'professional services': 'strategy',
    'data': 'data',
    'security': 'cybersecurity',
    'software and applications': 'software',
    'infrastructure': 'infrastructure',
    'support': 'support'
}
