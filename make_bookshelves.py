import HP
from API import add_bookshelves
import re


def create_bookshelves():
    """

    Create bookshelves from file HP.BOOK_SHELVES_LIST_PATH

    """
    f = open(HP.BOOK_SHELVES_LIST_PATH, "r")
    bookshelves_name = f.read()
    f.close()
    bookshelves_name = re.split(r'\n', bookshelves_name)
    add_bookshelves(bookshelves_name)


if __name__ == "__main__":
    create_bookshelves()