from gutenberg.query import get_metadata


class GutenbergBook(object):
    def __init__(self, id, metadata=None):
        """

        Args:
            id: the gutenberg ID
            metadata: (Optional) if it is not None it will construct Book from metadata.
                      metadata is a dictionary which includes ["title", "authors", "language", "bookshelves"]
        """
        if not isinstance(id, int):
            raise TypeError("id must be a positive integer")
        if id <= 0:
            raise TypeError("id must be a positive integer")
        self._id = id
        if metadata is None:
            self._title = list(get_metadata('title', self._id))[0]
            self._authors = list(get_metadata('author', self._id))
            self._language = list(get_metadata('language'))[0]
            self._bookshelves = set()
        else:
            self._title = metadata["title"]
            self._authors = metadata["author"]
            self._language = metadata["language"]
            self._bookshelves = metadata["bookshelves"]

    def __hash__(self):
        return hash(self._id)

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def authors(self):
        return self._authors.copy()

    @property
    def language(self):
        return self._language

    @property
    def bookshelves(self):
        return self._bookshelves.copy()

    @property
    def metadata(self):
        return {"title": self.title, "authors": self.authors,
                "language": self.language, "bookshelves": self.bookshelves}

    def add_bookshelf(self ,shelf):
        if not isinstance(shelf, str):
            raise TypeError("shelf should be a string")
        self._bookshelves = self._bookshelves | {shelf}


def create_gutenberg_books(inputs, dic=False):
    """

    Create a list of GutenbergBook objects from gutenberg ids or a metadata

    Args:
        inputs: either a set of integers which specify the ids or a dictionary including metadata for each gutenberg id
        dic: if True then the output will be in dictionary form {id: GutenbergBook(id)}

    Return:
        a set or dictionary of gutenberg books objects
    """
    if isinstance(inputs, set):
        res = {i: GutenbergBook(i) for i in inputs}
    elif isinstance(inputs, dict):
        res = {i: GutenbergBook(i, metadata) for i, metadata in inputs.items()}
    else:
        raise TypeError()
    if dic:
        return res
    else:
        return set(res.values())


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
            dc[x] = GutenbergBook(x).metadata
    return dc







