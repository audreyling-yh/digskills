import os
import re
import pandas as pd
import config

filepaths = config.filepaths


def get_filepath(key):
    path = filepaths[key]['folder'] + filepaths[key]['filename']
    return path


def get_ict_skills(tsc_df):
    # filter out not-purely-tech TSCs
    exclude_categories = ['Business Finance', 'General Management', 'People Development', 'Sales and Marketing',
                          'Stakeholder and Contract Management']
    tsc_df = tsc_df[~tsc_df['tsc_category'].isin(exclude_categories)]

    return tsc_df


def clean_abilities(text):
    # split abilities into one list element per bullet point
    abilities = text.split('•')
    abilities = [x.strip() for x in abilities]
    abilities = [x.lower() for x in abilities if x != '' and not x.isspace()]

    return abilities


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
    languages = [x.strip() for x in df[0].tolist()]
    languages = [x for x in languages if ' ' not in x]
    ngram_languages = [x for x in languages if ' ' in x]

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

        languages = ';'.join(languages_in_desc)

        extracted_languages.append(languages)

    return extracted_languages


def get_all_postings():
    jobs = pd.DataFrame()

    postings_folder = filepaths['mcf_jobpostings_final']['folder']
    cols = ['JOB_POST_ID', 'JOB_POST_DESC', 'AES', 'SSOC4D', 'SSOC1D', 'date', 'year', 'month', 'tsc_list', 'tsc_count',
            'tsc_category', 'tsc_category_count', 'programming_languages']

    for i in os.listdir(postings_folder):
        print('Reading {}'.format(i))

        df = pd.read_csv(postings_folder + i, usecols=cols)
        jobs = jobs.append(df)

    jobs.drop_duplicates(inplace=True)

    # clean
    jobs['year'] = jobs['year'].apply(str)

    return jobs


def save_csv(df, filepath, index=False):
    df.to_csv(filepath, index=index)


def get_all_unique_tsc_categories():
    ict_skills_filepath = config.filepaths['ssg_ict_skills_original']['folder'] + \
                          config.filepaths['ssg_ict_skills_original']['filename']
    ict_skills = pd.read_csv(ict_skills_filepath)
    ict_skills = get_ict_skills(ict_skills)

    categories = ict_skills['tsc_category'].unique()

    return categories
