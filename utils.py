import itertools


def chunk_iterable(iterable, size=10):
    """Chunk an iterable into uniform batch sizes

    :param iterable: iterable to chunk
    :param size: chunk size
    :return: generator of chunks
    """
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))
