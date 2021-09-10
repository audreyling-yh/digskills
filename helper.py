import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import config
import torch

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


def bert_text_preparation(text, tokenizer):
    """Preparing the input for BERT

    Takes a string argument and performs
    pre-processing like adding special tokens,
    tokenization, tokens to ids, and tokens to
    segment ids. All tokens are mapped to seg-
    ment id = 1.

    Args:
        text (str): Text to be converted
        tokenizer (obj): Tokenizer object
            to convert text into BERT-re-
            adable tokens and ids

    Returns:
        list: List of BERT-readable tokens
        obj: Torch tensor with token ids
        obj: Torch tensor segment ids
    """
    marked_text = "[CLS] " + str(text) + " [SEP]"
    tokenized_text = tokenizer.tokenize(marked_text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

    # Truncate vector to 512 elements to fit BERT tensor limit
    if len(indexed_tokens) > 512:
        indexed_tokens = indexed_tokens[:512]

    segments_ids = [1] * len(indexed_tokens)

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])

    return tokenized_text, tokens_tensor, segments_tensors


def get_bert_embeddings(tokens_tensor, segments_tensors, model):
    """Get embeddings from an embedding model

    Args:
        tokens_tensor (obj): Torch tensor size [n_tokens]
            with token ids for each token in text
        segments_tensors (obj): Torch tensor size [n_tokens]
            with segment ids for each token in text
        model (obj): Embedding model to generate embeddings
            from token and segment ids

    Returns:
        list: List of list of floats of size
            [n_tokens, n_embedding_dimensions]
            containing embeddings for each token

    """
    # Activate GPU if any
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    tokens_tensor = tokens_tensor.to(device)
    segments_tensors = segments_tensors.to(device)
    model = model.to(device)

    # Gradient calculation id disabled
    # Model is in inference mode
    with torch.no_grad():
        outputs = model(input_ids=tokens_tensor,
                        token_type_ids=segments_tensors,
                        output_hidden_states=True)

        # Removing the first hidden state
        # The first state is the input state
        # BERT has 12 hidden layers in total
        hidden_states = outputs.hidden_states[1:]

    # Getting embeddings from the final BERT layer
    token_embeddings = hidden_states[-1]

    # Get sentence embedding using mean pooling
    token_embeddings = torch.mean(token_embeddings[0], dim=0).to(device)

    # Converting torchtensors to lists
    list_token_embeddings = [token_embed.tolist() for token_embed in token_embeddings]

    return list_token_embeddings
