from gutenberg_book import GutenbergBook, book_metadata
import gutenberg.query as gq


def metadata(book_id):
    """

    Args:
        book_id: book id (integer)

    Returns:
        metadata of that book: a dictionary with keys ["title", "authors", "language", "bookshelves"],
                                which bookshelves is an empty set
    """
    title = {str(x) for x in gq.get_metadata('title', book_id)}
    authors = {str(x) for x in gq.get_metadata('author', book_id)}
    language = {str(x) for x in gq.get_metadata('language', book_id)}
    bookshelves = set()
    return book_metadata(book_id, title, authors, language, bookshelves)


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
