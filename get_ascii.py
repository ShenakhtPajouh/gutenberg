import API
import HP

def set_ascii():
    books = API.get_books()
    new_books = []
    for id, book in books.items():
        path = HP.BOOKS_PATH + str(id) + ".txt"
        with open(path, 'r') as f:
            text = f.read()
        try:
            text = text.decode('UTF-8')
            book.add_bookshelf('ascii')
            new_books.append(book)
        except UnicodeDecodeError:
            continue
    print len(new_books)
    API.add_books(new_books)

