import HP
from API import download_books
from os.path import isfile
import pickle


def download_all_books():
    """

    Download all books in books_id

    """
    if isfile(HP.BOOKS_ID_PATH):
        f = open(HP.BOOKS_ID_PATH, "rb")
        books_id = pickle.load(f)
        assert isinstance(books_id, set)
        download_books(books_id)


if __name__ == "__main__":
    download_all_books()
