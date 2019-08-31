import itertools
import re


def chunk_iterable(iterable, size=10):
    """Chunk an iterable into uniform batch sizes

    :param iterable: iterable to chunk
    :param size: chunk size
    :return: generator of chunks
    """
    iterator = iter(iterable)
    for first in iterator:
        yield itertools.chain([first], itertools.islice(iterator, size - 1))


def insert_line_breaks(s, line_char_width=32, line_break='<br>'):
    """Inserted linebreak every n characters

    Intended for use with plotly hover information (reason for line_break default value)

    :param s: string to insert line breaks into
    :param line_char_width: number of characters per line
    :param line_break: string to be inserted as linebreak
    :return: string with linebreaks inserted every n chars
    """
    return re.sub(f'(.{{{line_char_width},}})?\\s', f'\\1{line_break}', s, 0, re.DOTALL)
