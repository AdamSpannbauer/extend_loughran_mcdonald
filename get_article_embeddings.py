import json
import pandas as pd
from nltk import sent_tokenize
from universal_sentence_encoder import get_sentence_embeddings

ARTICLES_JSON_PATH = 'data/articles.json'
EMBEDDINGS_CSV_PATH = 'data/article_embeddings.csv'

with open(ARTICLES_JSON_PATH, 'r') as f:
    articles = json.load(f)['articles']

articles_df = pd.DataFrame(articles)
articles_df = articles_df.explode('text')
articles_df['text'] = articles_df['text'].apply(sent_tokenize)
articles_df = articles_df.explode('text')
articles_df['text'] = articles_df['text'].str.strip()

# Duplicated text across will be assumed to be boilerplate
# 100 is pretty arbitrary (300 total articles when chosen)
article_text_df = articles_df.groupby(['text']).size().reset_index(name='count')
article_text_df = article_text_df.loc[article_text_df['count'] < 100]

article_embeddings = get_sentence_embeddings(article_text_df['text'].tolist(), chunk_size=512)  # base 2 to look smart
article_embeddings_df = pd.DataFrame(article_embeddings)
article_embeddings_df['text'] = article_text_df['text']
article_embeddings_df.to_csv(EMBEDDINGS_CSV_PATH, index=False)
