import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
import plotly_express as px
import plotly.offline as py
from loughran_mcdonald_helpers import tag_financial_sentiment
from utils import insert_line_breaks

EMBEDDINGS_CSV_PATH = 'data/article_embeddings.csv'

article_embeddings_df = pd.read_csv(EMBEDDINGS_CSV_PATH, header=0)

# Features from universal sentence encoder are numbered 0-511
embeddings_columns = [str(i) for i in range(512)]
embeddings_arr = np.array(article_embeddings_df[embeddings_columns])

embeddings_2d_arr = TSNE(n_components=2, random_state=1).fit_transform(embeddings_arr)
embeddings_2d_df = pd.DataFrame(embeddings_2d_arr, columns=['embed_1', 'embed_2'])

# Color sentences in plot by dictionary tagged sentiment
embeddings_2d_df['text'] = article_embeddings_df['text']
embeddings_2d_df['sentiment'] = tag_financial_sentiment(embeddings_2d_df['text'])
embeddings_2d_df = embeddings_2d_df.explode('sentiment')
embeddings_2d_df['sentiment'] = embeddings_2d_df['sentiment'].fillna('none')

# Add html line breaks to display better in plotly hover
embeddings_2d_df['text'] = embeddings_2d_df['text'].fillna('')
embeddings_2d_df['text'] = embeddings_2d_df['text'].apply(insert_line_breaks)

fig = px.scatter(embeddings_2d_df,
                 x='embed_1',
                 y='embed_2',
                 color='sentiment',
                 hover_name='text',
                 opacity=0.7)
py.plot(fig, config={'displayModeBar': False})
