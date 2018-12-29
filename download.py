from API import get_books, download_books


def download_all_books():
    """

    Download all books in books_id

    """
    books_id = get_books(book_object=False).keys()
    download_books(books_id)


if __name__ == "__main__":
    download_all_books()
