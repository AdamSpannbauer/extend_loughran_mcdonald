import warnings
import pandas as pd

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


if __name__ == '__main__':
    lm_sentiment_df = load_loughran_mcdonald()
    print(lm_sentiment_df)
