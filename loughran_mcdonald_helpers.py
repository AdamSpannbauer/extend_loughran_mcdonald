import re
import warnings
import pandas as pd
import numpy as np

WORD_LIST_XLSX_PATH = 'data/LoughranMcDonald_SentimentWordLists_2018.xlsx'

LICENSE_REQUIRED_DISCLAIMER = """
License required for commercial use of Loughran-McDonald Sentiment lexicon.
Please contact tloughra@nd.edu.

Downloaded from: https://sraf.nd.edu/textual-analysis/resources/ 
"""


def load_loughran_mcdonald(xlsx_path=WORD_LIST_XLSX_PATH):
    warnings.warn(LICENSE_REQUIRED_DISCLAIMER)

    sheet_df_dict = pd.read_excel(xlsx_path, sheet_name=None, header=None)

    sheet_df_list = []
    for sheet_name, sheet_df in sheet_df_dict.items():
        if sheet_name == 'Documentation':  # Never read documentation....
            continue

        sheet_df.columns = ['word']
        sheet_df['sentiment'] = sheet_name.lower()
        sheet_df_list.append(sheet_df)

    sentiment_df = pd.concat(sheet_df_list)
    sentiment_df.word = sentiment_df.word.str.lower()

    return sentiment_df


def _tokenize(text):
    """Split text into tokens using a regular expression

    This is a wrapper for ``re.findall`` with case ignored.

    :param text: text to be tokenized
    :return: a list of resulting tokens

    >>> tokenize("word word 1.22 can't. cannot")
    ['word', 'word', 'can', 't', 'cannot']
    """
    default = [np.nan]

    if pd.isna(text):
        return default

    tokens = re.findall(r'@?#?[a-zA-z]+', text, flags=re.IGNORECASE)

    if not tokens:
        return default

    return tokens


def _collapse_sentiment_tags(tags):
    return list(set(tag for tag in tags.tolist() if not pd.isna(tag)))


def tag_financial_sentiment(text):
    """Tag text w/loughran mcdonald sentiment dictionary

    :param text: list-like object of text
    :return: set w/len equal to text containing lists of tags
    """
    token_df_list = []
    for i, t in enumerate(text):
        token_list = _tokenize(t)
        token_df_i = pd.DataFrame({'doc_id': i, 'word': token_list})
        token_df_list.append(token_df_i)

    token_df = pd.concat(token_df_list)
    # TODO: don't re-read this every time
    lm_sentiment_df = load_loughran_mcdonald()

    tagged_token_df = pd.merge(token_df, lm_sentiment_df, how='left', on='word')
    tag_list_series = tagged_token_df.groupby('doc_id')['sentiment'].apply(_collapse_sentiment_tags)

    return tag_list_series.tolist()


if __name__ == '__main__':
    text_list = [
        'It was an unprofitable quarter for the company.',
        'The market is as volatile as ever.',
        'The CEO is being acquitted of all aforementioned charges.',
        'zzz'
    ]
    sentiment_tags = tag_financial_sentiment(text_list)

    tagged_text_df = pd.DataFrame({
        'text': text_list,
        'sentiment': sentiment_tags
    })
    print(tagged_text_df)
