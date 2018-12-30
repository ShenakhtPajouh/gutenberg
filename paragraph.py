class Paragraph(object):
    def __init__(self, id, text, book_id=None, next_id=None, prev_id=None, tags=dict()):
        assert isinstance(id, int)
        assert id > 0
        if book_id is not None:
            assert book_id > 0
        if next_id is not None:
            assert next_id > 0
        if prev_id is not None:
            assert prev_id > 0
        assert isinstance(tags, dict)
        assert isinstance(text, list)
        assert all([isinstance(sent, list) for sent in text])
        assert all([all([isinstance(word, str) for word in sent]) for sent in text])
        self._id = id
        self._text = text
        self._book_id = book_id
        self._tags = tags
        self._next_id = next_id
        self._prev_id = prev_id

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        text = sum(self._text, [])
        return " ".join(text)

    @property
    def has_book(self):
        return self._book_id is not None

    @property
    def book_id(self):
        return self._book_id

    @property
    def next_id(self):
        return self._next_id
    @property
    def prev_id(self):
        return self._prev_id

    @property
    def tags(self):
        return self._tags.copy()

    def add_tag(self, new_tags):
        if isinstance(new_tags, int):
            new_tags = {new_tags}
        self._tags = self._tags | set(new_tags)

    @property
    def metadata(self):
        return paragraph_metadata(self.id, self.book_id, self.prev_id, self.next_id, self.tags)

    @property
    def sentences(self):
        return [sent.copy() for sent in self._text]

    @property
    def words(self):
        return sum(self._text, [])


def paragraph_metadata(id=None, book_id=None, prev_id=None, next_id=None,tags=None):
    """

    A helper for creating metadata

    Args:
        book_id, tags are either string or simple list, set or ... of strings.
        if one of them is None, it will be ignored in return

    Returns:
         a dictionary of metadata form for a book with keys which are given

    """
    res = dict()

    x = id
    name = "id"
    if x is not None:
        if isinstance(x, int):
            res[name] = {x}
        else:
            assert len(x) == 1
            assert all([isinstance(s, int) for s in x])
            res[name] = set(x)

    x = book_id
    name = "book_id"
    if x is not None:
        if isinstance(x, int):
            res[name] = {x}
        else:
            assert len(x) == 1
            assert all([isinstance(s, int) for s in x])
            res[name] = set(x)

    x = prev_id
    name = "prev_id"
    if x is not None:
        if isinstance(x, int):
            res[name] = {x}
        else:
            assert len(x) == 1
            assert all([isinstance(s, int) for s in x])
            res[name] = set(x)

    x = next_id
    name = "next_id"
    if x is not None:
        if isinstance(x, int):
            res[name] = {x}
        else:
            assert len(x) == 1
            assert all([isinstance(s, int) for s in x])
            res[name] = set(x)

    x = tags
    name = "tags"
    if x is not None:
        if isinstance(x, int):
            res[name] = {x}
        else:
            assert all([isinstance(s, int) for s in x])
            res[name] = set(x)

    return res



