class GutenbergBook(object):
    def __init__(self, id, metadata):
        """

        Args:
            id: the gutenberg ID
            metadata: metadata is a dictionary which includes ["title", "authors", "language", "bookshelves"]
        """
        if not isinstance(id, int):
            raise TypeError("id must be a positive integer")
        if id <= 0:
            raise TypeError("id must be a positive integer")
        self._id = id
        self._title = metadata["title"]
        self._authors = metadata["authors"]
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

    def add_bookshelf(self, shelf):
        if not isinstance(shelf, str):
            raise TypeError("shelf should be a string")
        self._bookshelves = self._bookshelves | {shelf}


def create_gutenberg_books(inputs, dic=False):
    """

    Create a list of GutenbergBook objects from gutenberg ids or a metadata

    Args:
        inputs: a dictionary including metadata for each gutenberg id {id: metadata(id)}
        dic: if True then the output will be in dictionary form {id: GutenbergBook(id)}

    Return:
        a set or dictionary of gutenberg books objects
    """
    if not isinstance(inputs, dict):
        raise TypeError("inputs must be a dictionary")
    res = {i: GutenbergBook(i, metadata) for i, metadata in inputs.items()}
    if dic:
        return res
    else:
        return set(res.values())





