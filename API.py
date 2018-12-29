import HP
import pickle
from os.path import isfile
from gutenberg_objects import *
from gather_info import *
from collections import defaultdict
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from metadata import create_metadata


def get_books(books_list=None, books_features=None, book_object=True):
    """

    Args:
        books_list: (Optional) list of books gutenberg ID to create books. if it is None then it will return all books.
        books_features: (Optional) features to get books with that feature. a dictionary which values are set or list.
        book_object: if it is True then returns GutenbergBooks else it will return metadata

    Returns:
         a dictionary of books objects {id: GutenbergBook(id)/metadata(id)}
    """
    if books_list is not None and books_features is not None:
        raise AttributeError("only one of books_list and books_features should be identified")
    if isfile(HP.BOOKS_DATA_PATH):
        pk = open(HP.BOOKS_DATA_PATH, "rb")
        books_metadata = pickle.load(pk)
        pk.close()
        assert isinstance(books_metadata, dict)

    else:
        books_metadata = dict()

    if books_list is not None:
        books_list = books_list & set(books_metadata)
        books_metadata = {id: books_metadata[id] for id in books_list}
    if books_features is not None:
        for feature, items in books_features.items():
            books_metadata = {id: metadata for id, metadata in books_metadata.items()
                              if items.issubset(metadata[feature])}
    if book_object:
        return create_gutenberg_books(books_metadata, dic=True)
    return books_metadata


def add_books(books_list):
    """

    Add books to dataset

    Args:
        books_list: a set of books id or GutenbergBooks

    """
    gb_list = {book for book in books_list if isinstance(book, GutenbergBook)}
    id_list = {book for book in books_list if isinstance(book, int)}
    books = get_books()
    id_list = id_list - set(books)
    assert all([isvalid(i) for i in id_list])
    new_metadata_id = create_metadata(id_list)
    new_books = gb_list | create_gutenberg_books(new_metadata_id)
    for book in new_books:
        books[book.id] = book
    pk = open(HP.BOOKS_DATA_PATH, "wb")
    pickle.dump(create_metadata(books.values()), pk)
    pk.close()


def get_bookshelves(bookshelves_list=None):
    """

    Args:
        bookshelves_list: (Optional) list of bookshelves to return. if it is None then it will return all bookshelves

    Returns:
        a dictionary of bookshelves {bookshelf: bookshelf_elements_id}

    """
    if isfile(HP.BOOK_SHELVES_PATH):
        pk = open(HP.BOOK_SHELVES_PATH, "rb")
        bookshelves = pickle.load(pk)
        pk.close()
        assert isinstance(bookshelves, dict)
        if bookshelves_list is not None:
            bookshelves_list = bookshelves_list & set(bookshelves)
            bookshelves = {bookshelf: bookshelves[bookshelf] for bookshelf in bookshelves_list}
    else:
        bookshelves = dict()
    return bookshelves


def add_bookshelves(new_bookshelves):
    """

    Get all books in bookshelf <name> and update metadata

    Args:
        new_bookshelves: a dictionary {bookshelf_name: {id of bookshelf's books}}

    Returns:
          None

    """
    assert isinstance(new_bookshelves, dict)
    bookshelves = defaultdict(lambda: set(), get_bookshelves())
    new_ids = set.union(*new_bookshelves.values())
    books = get_books(new_ids)
    new_books = create_metadata(new_ids - set(books))
    new_books = create_gutenberg_books(new_books, dic=True)
    books = dict(books.items() + new_books.items())
    for bookshelf, bookshelf_ids in new_bookshelves.items():
        bookshelves[bookshelf] = bookshelves[bookshelf] | bookshelf_ids
        for id in bookshelf_ids:
            books[id].add_bookshelf(bookshelf)
    add_books(books.values())
    with open(HP.BOOK_SHELVES_PATH, "wb") as f:
        pickle.dump(dict(bookshelves), f)


def download_books(books, rewrite=False, ignore_invalid_books=True):
    """

    Download all books in books and save the text in file HP.BOOKS_PATH/<book id>.txt .

    Args:
        books: a list of ids or GutenbergBooks
        rewrite: (Optional) if True rewrite the existing files
        ignore_invalid_books: (Optional) if True then it will ignore invalid books

    """
    for book in books:
        if isinstance(book, GutenbergBook):
            id = book.id
        else:
            id = book
        if not isvalid(id):
            if ignore_invalid_books:
                continue
            else:
                raise AttributeError("invalid book id")
        path = HP.BOOKS_PATH + str(id) + ".txt"
        if (not rewrite) and isfile(path):
            continue
        text = strip_headers(load_etext(id)).strip().encode('UTF-8')
        f = open(path, "w")
        f.write(text)
        f.close()








