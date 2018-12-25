import HP
import pickle
from os.path import isfile
from gutenberg_objects import *
from gather_info import *
from collections import defaultdict
from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers


def get_books():
    """

    Returns:
         a dictionary of books objects {id: GutenbergBook(id)}
    """
    if isfile(HP.BOOKS_ID_PATH):
        pk = open(HP.BOOKS_ID_PATH, "rb")
        books_id = pickle.load(pk)
        pk.close()
        assert isinstance(books_id, set)
    else:
        books_id = set()

    if isfile(HP.BOOKS_DATA_PATH):
        pk = open(HP.BOOKS_DATA_PATH, "rb")
        books_metadata = pickle.load(pk)
        pk.close()
        assert isinstance(books_metadata, dict)
    else:
        books_metadata = dict()

    books_id = books_id | set(books_metadata)
    books = create_gutenberg_books(books_metadata) | create_gutenberg_books(books_id - set(books_metadata))
    return {b.id: b for b in books}


def get_bookshelves():
    """

    Returns:
        a dictionary of bookshelves {bookshelf: bookshelf_elements_id}

    """
    if isfile(HP.BOOK_SHELVES_PATH):
        pk = open(HP.BOOK_SHELVES_PATH, "rb")
        bookshelves = pickle.load(pk)
        pk.close()
        assert isinstance(bookshelves, dict)
        bookshelves = defaultdict(lambda: set(), bookshelves)
    else:
        bookshelves = defaultdict(lambda: set())
    return bookshelves


def add_bookshelves(bookshelves_names):
    """

    Get all books in bookshelf <name> and update metadata

    Args:
        bookshelves_names: a list of bookshelfves name. note that there should be raw text file of that bookshelf page
                           in HP.PAGES_PATH/<name>.txt

    Returns:
          None

    """
    new_bookshelves = dict()
    for name in bookshelves_names:
        f = open(HP.PAGES_PATH + name + ".txt", "r")
        text = f.read()
        f.close()
        ids = find_books_html(text)
        ids = [id for id in ids if isvalid(id)]
        new_bookshelves[name] = ids

    bookshelves = get_bookshelves()
    books = get_books()
    for bookshelf in new_bookshelves:
        new_bookshelves[bookshelf] = new_bookshelves[bookshelf] - bookshelves[bookshelf]
        bookshelves[bookshelf] = bookshelves[bookshelf] | new_bookshelves[bookshelf]
        for id in new_bookshelves[bookshelf]:
            books[id].add_bookshelf(bookshelf)

    books = create_metadata(books)

    with open(HP.BOOKS_DATA_PATH, "wb") as f:
        pickle.dump(books, f)
        f.close()

    with open(HP.BOOKS_ID_PATH, "wb") as f:
        pickle.dump(set(books.keys()), f)
        f.close()

    with open(HP.BOOK_SHELVES_PATH, "wb") as f:
        pickle.dump(dict(bookshelves))
        f.close()


def download_books(books, rewrite=False, ignore_invalid_books = True):
    """

    Download all books in books and save the text in file HP.BOOKS_PATH/<book id>.txt .

    Args:
        books: a list of ids or GutenbergBooks
        rewrite: if True rewrite the existing files
        ignore_invalid_books: if True then it will ignore invalid books

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
                raise TypeError("invalid book id")
        path = HP.BOOKS_PATH + str(id) + ".txt"
        if not rewrite and isfile(path):
            continue
        text = strip_headers(load_etext(id)).strip().encode('UTF-8')
        f = open(path, "w")
        f.write(text)
        f.close()








