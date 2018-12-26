import HP
from API import add_bookshelves
import re
from os.path import isfile
from gather_info import find_books_html, isvalid


def create_bookshelves():
    """

    Create bookshelves from file HP.BOOK_SHELVES_LIST_PATH
    note that there should be raw text file of that bookshelf page in HP.PAGES_PATH/<name>.txt

    """
    f = open(HP.BOOK_SHELVES_LIST_PATH, "r")
    bookshelves_names = f.read()
    f.close()
    bookshelves_names = re.split(r'\n', bookshelves_names)
    new_bookshelves = dict()
    for name in bookshelves_names:
        if not isfile(HP.PAGES_PATH + name + ".txt"):
            continue
        f = open(HP.PAGES_PATH + name + ".txt", "r")
        text = f.read()
        f.close()
        ids = find_books_html(text)
        ids = {id for id in ids if isvalid(id)}
        new_bookshelves[name] = ids
    add_bookshelves(new_bookshelves)


if __name__ == "__main__":
    create_bookshelves()
