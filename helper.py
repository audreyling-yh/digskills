import ast
import os
import re
import pandas as pd
import config

filepaths = config.filepaths


def get_filepath(key):
    path = filepaths[key]['folder'] + filepaths[key]['filename']
    return path


def get_ict_skills(tsc_df):
    # filter out not-purely-tech TSC categories
    exclude_categories = ['Business and Project Management', 'Business Finance', 'General Management',
                          'Governance and Compliance', 'People Development', 'Sales and Marketing',
                          'Stakeholder and Contract Management']
    tsc_df = tsc_df[~tsc_df['tsc_category'].isin(exclude_categories)]

    # filter out by skill
    exclude_tscs = ['Organisational Design', 'Networking', 'Business Negotiation']
    tsc_df = tsc_df[~tsc_df['tsc_title'].isin(exclude_tscs)]

    return tsc_df


def indicate_ict_job(df):
    filepath = get_filepath('digital_jobs_ssoc')

    # get ICT SSOCs
    ict_jobs = pd.read_csv(filepath)
    ict_ssoc = ict_jobs['SSOC 2020'].unique().tolist()

    # true if the job's SSOC is an ICT SSOC
    df['ict'] = df['SSOC 2020'].isin(ict_ssoc)

    return df


def read_txt(filepath):
    # read text into string
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        text = ' '.join([x.strip() for x in lines])

    return text


def extract_programming_languages(series):
    # get list of programming languages
    filepath = get_filepath('programming_languages')
    df = pd.read_csv(filepath, header=None)
    planguages = [x.strip() for x in df[0].tolist()]
    languages = [x for x in planguages if ' ' not in x]
    ngram_languages = [x for x in planguages if ' ' in x]

    # extract language from each job posting/resume
    extracted_languages = []
    for i in series:
        languages_in_desc = []

        # title case job description/resume
        if i.isupper() or i.islower():
            i = i.title()

        # get single word programming languages from job description/resume
        tokens = re.findall(r'[^,?():;/{}!.\s]+', i)
        languages_in_desc += [x for x in languages if x in tokens]

        # get multiple word programming languages from job description/resume
        languages_in_desc += [x for x in ngram_languages if x in i]

        languages_in_desc = ';'.join(languages_in_desc)

        extracted_languages.append(languages_in_desc)

    return extracted_languages


def get_all_postings():
    jobs = pd.DataFrame()

    postings_folder = filepaths['mcf_jobpostings_final']['folder']
    cols = ['JOB_POST_ID', 'JOB_POST_DESC', 'AES', 'SSOC 2020', 'date', 'year', 'month', 'tsc_list', 'tsc_count',
            'programming_languages']

    for i in os.listdir(postings_folder):
        print('Reading {}'.format(i))

        df = pd.read_csv(postings_folder + i, usecols=cols)
        jobs = jobs.append(df)

    # clean
    jobs['year'] = jobs['year'].apply(str)
    jobs['tsc_list'] = jobs['tsc_list'].apply(ast.literal_eval)
    jobs['programming_languages'] = jobs['programming_languages'].apply(
        lambda x: x.split(';') if type(x) == str else [])
    jobs['pl_count'] = jobs['programming_languages'].apply(len)

    return jobs


def get_1q21_data(resumes=False):
    df = pd.DataFrame()

    if resumes:
        folder = filepaths['resumes_final']['folder']
        cols = ['file', 'resume', 'programming_languages', 'month', 'year', 'YYYYMM', 'tsc_list', 'tsc_count']
    else:
        folder = filepaths['mcf_jobpostings_final']['folder']
        cols = ['JOB_POST_ID', 'JOB_POST_DESC', 'AES', 'SSOC 2020', 'date', 'year', 'month', 'tsc_list', 'tsc_count',
                'programming_languages']

    periods = ['202101', '202102', '202103']
    for i in os.listdir(folder):
        if any(x in i for x in periods):
            print('Reading {}'.format(i))

            temp = pd.read_csv(folder + i, usecols=cols)
            df = df.append(temp)

    # prep
    df['year'] = df['year'].apply(str)
    df['tsc_list'] = df['tsc_list'].apply(ast.literal_eval)
    df['programming_languages'] = df['programming_languages'].apply(lambda x: x.split(';') if type(x) == str else [])

    return df


def save_csv(df, filepath, index=False):
    df.to_csv(filepath, index=index)
