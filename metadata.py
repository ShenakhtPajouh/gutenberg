from gutenberg_objects import GutenbergBook, gutenberg_metadata
import gutenberg.query as gq
from gather_info import isvalid


def metadata(book_id):
    """

    Args:
        book_id: book id (integer)

    Returns:
        metadata of that book: a dictionary with keys ["title", "authors", "language", "bookshelves"],
                                which bookshelves is an empty set
    """
    assert isvalid(book_id)
    title = set(gq.get_metadata('title', book_id))
    authors = set(gq.get_metadata('author', book_id))
    language = set(gq.get_metadata('language', book_id))
    bookshelves = set()
    return gutenberg_metadata(title, authors, language, bookshelves)


def create_metadata(inputs):
    """

    Create metadata file from list of ids or GutenbergBooks

    Args:
        inputs: a list or set of integers or GutenbergBooks

    Return:
        a dictionary which create metadata for each gutenberg book
    """
    dc = dict()
    for x in inputs:
        if isinstance(x, GutenbergBook):
            dc[x.id] = x.metadata
        else:
            dc[x] = metadata(x)
    return dc
