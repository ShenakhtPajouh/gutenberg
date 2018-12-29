
def paragraph_tags():
    raise NotImplementedError

def get_tag(tag):
    """

    Args:
        tag: either an int or str

    Returns:
        if tag is int the name (str) of tag else the int_code of tag

    """
    tags = paragraph_tags()
    if tag is int:
        return tags[tag]
    ls = [i for i, s in tags.items() if s == tag]
    if len(ls) == 0:
        raise ValueError("tag is not listed in tags")
    return ls[0]


class Paragraph(object):
    def __init__(self, id, text, book_id=None, tags=dict()):
        assert isinstance(id, int)
        assert id > 0
        assert isinstance(text, str)
        if book_id is not None:
            assert book_id > 0
        assert isinstance(tags, dict)
        self._id = id
        self._text = text
        self._book_id = book_id
        self._tags = tags

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def has_book(self):
        return self._book_id is not None

    @property
    def book_id(self):
        if self.has_book:
            return self._book_id
        return 0

    @property
    def tags(self):
        return self._tags.copy()

    def add_tag(self, new_tags):
        self._tags = self._tags | set(new_tags)

    @property
    def metadata(self):
        raise NotImplementedError


def paragraph_metadata(book_id=None, tags=None):
    """

    A helper for creating metadata

    Args:
        book_id, tags are either string or simple list, set or ... of strings.
        if one of them is None, it will be ignored in return

    Returns:
         a dictionary of metadata form for a book with keys which are given

    """
    res = dict()

    x = book_id
    name = "book_id"
    if x is not None:
        if isinstance(x, int):
            res[name] = {x}
        else:
            assert len(x) == 1
            assert all([isinstance(s, int) for s in x])
            res[name] = set(x)
