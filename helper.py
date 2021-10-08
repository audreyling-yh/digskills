import os
import pandas as pd
import config

filepaths = config.filepaths


def get_ict_skills(tsc_df):
    # filter out not-purely-tech TSCs
    exclude_categories = ['Business Finance', 'General Management', 'People Management', 'Sales and Marketing',
                          'Stakeholder and Contract Management']
    tsc_df = tsc_df[~tsc_df['tsc_category'].isin(exclude_categories)]

    return tsc_df


def clean_abilities(text):
    # split abilities into one list element per bullet point
    abilities = text.split('•')
    abilities = [x.strip() for x in abilities]
    abilities = [x.lower() for x in abilities if x != '' and not x.isspace()]

    return abilities


def get_all_postings():
    jobs = pd.DataFrame()

    postings_folder = filepaths['mcf_jobpostings_final']['folder']
    cols = ['JOB_POST_ID', 'JOB_POST_DESC', 'AES', 'SSOC4D', 'SSOC1D', 'date', 'year', 'month', 'tsc_list', 'tsc_count',
            'tsc_category', 'tsc_category_count']

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
