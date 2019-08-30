import os
import tqdm
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from utils import chunk_iterable

# tensorflow_hub typically caches model in a tmp dir
# Redirect cache to sentence_encoder_cache dir for future use w/o re-downloading
os.environ["TFHUB_CACHE_DIR"] = "sentence_encoder_cache"

# Import the Universal Sentence Encoder's TF Hub module
module_url = "https://tfhub.dev/google/universal-sentence-encoder-large/3"
embed = hub.Module(module_url)


def _get_sentence_embeddings(sentence_list):
    """Apply Universal Sentence Encoder to embed sentences

    :param sentence_list: list of str sentences to get embeddings for
    :return: np array of shape (len(sentence_list), 512) containing embeddings

    >>> x = get_sentence_embeddings(['Functions need testing.', 'Testing uses test data.', 'Why not a haiku?'])
    >>> x.shape
    (3, 512)
    >>> x.dtype
    dtype('float32')
    """
    with tf.Session() as session:
        session.run([tf.global_variables_initializer(), tf.tables_initializer()])
        embeddings = session.run(embed(sentence_list))

    return embeddings


def get_sentence_embeddings(sentence_list, chunk_size=100, progress=True):
    """Apply Universal Sentence Encoder to embed sentences

    :param sentence_list: list of str sentences to get embeddings for
    :param chunk_size: how many sentences should be processed at a time
    :param progress: Print tqdm progress bar?
    :return: np array of shape (len(sentence_list), 512) containing embeddings

    >>> x = get_sentence_embeddings(['Functions need testing.', 'Testing uses test data.', 'Why not a haiku?'])
    >>> x.shape
    (3, 512)
    >>> x.dtype
    dtype('float32')
    """
    chunks = chunk_iterable(sentence_list, size=chunk_size)

    enumerator = enumerate(chunks)
    if progress:
        enumerator = tqdm.tqdm(enumerator)

    embeddings_list = []
    for i, chunk in enumerator:
        sentence_list_chunk = list(chunk)
        embeddings_i = _get_sentence_embeddings(sentence_list_chunk)
        embeddings_list.append(embeddings_i)

    return np.vstack(embeddings_list)
