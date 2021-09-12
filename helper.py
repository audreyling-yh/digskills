import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import config

filepaths = config.filepaths


def get_all_postings():
    jobs = pd.DataFrame()

    postings_folder = filepaths['mcf_jobpostings_digital_tracks']['folder']
    cols = ['JOB_POST_ID', 'AES', 'SSOC4D', 'SSOC1D', 'date', 'year', 'skill_list', 'tracks_count',
            'subtracks_count', 'tracks_final', 'num_tracks_final', 'subtracks_final', 'num_subtracks_final']

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


def scale_counts(df, colname):
    newcolname = 'scaled_' + colname
    df[newcolname] = df.apply(
        lambda x: x[colname] * 4 if x['year'] == '2018'
        else x[colname] * 3 if x['year'] == '2021'
        else x[colname], axis=1)

    return df


def lineplot(df, x_col, y_col, x_label, y_label, title, img_name, hue_col=False, style_col=False,
             palette='Set2', legendloc='bottom', figsize=(6, 4), legendtitle=''):
    sns.set_style('whitegrid')

    fig, ax = plt.subplots(figsize=figsize)

    if hue_col and style_col:
        sns.lineplot(data=df, x=x_col, y=y_col, hue=hue_col, style=style_col, palette=palette)
    elif hue_col:
        sns.lineplot(data=df, x=x_col, y=y_col, hue=hue_col, palette=palette)
    else:
        sns.lineplot(data=df, x=x_col, y=y_col, palette=palette)

    sns.despine(top=True, right=True, left=True, bottom=True)

    if legendloc == 'right':
        ax.legend(title=legendtitle, loc='center left', bbox_to_anchor=(1, 0.5))

    ax.set_ylim(bottom=0)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.tight_layout()

    img_filepath = filepaths['img']['folder'] + filepaths['img']['filename']
    plt.savefig(img_filepath.format(img_name))
    plt.close()
