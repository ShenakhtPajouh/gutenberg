from paragraph import *
import API
import HP
from paragraph_analyse import tagger
import pickle
import os
import sys

def make_paragraphs(books_list=None):
    """

    Create paragraphs from available books

    Args:
        books_list: (Optional) if it is None, only paragraphs from the list will be created

    """
    books = set(API.get_books(books_list))
    paragraphs = dict()
    index = 0
    for book_id in books:
        pars = API.get_paragraphs_from_book(book_id, False)
        prev_par = None
        for t in pars:
            index = index + 1
            par = Paragraph(text=t, id=index, book_id=book_id, tags=tagger(t))
            if prev_par is not None:
                prev_par.next_id = par.id
                par.prev_id = prev_par.id
            prev_par = par
            paragraphs[index] = par
    paragraphs_metadata = {id: par.metadata for id, par in paragraphs.items()}
    paragraphs = {paragraph.id: paragraph.sentences for paragraph in paragraphs.values()}
    path = os.path.dirname(HP.PARAGRAPH_DATA_PATH)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(HP.PARAGRAPH_DATA_PATH, "wb") as pkl:
        pickle.dump(paragraphs, pkl)
    path = os.path.dirname(HP.PARAGRAPH_METADATA_PATH)
    if not os.path.exists(path):
        os.makedirs(path)
    with open(HP.PARAGRAPH_METADATA_PATH, "wb") as pkl:
        pickle.dump(paragraphs_metadata, pkl)


if __name__ == "__main__":
    # sys.setdefaultencoding() does not exist, here!
    reload(sys)  # Reload does the trick!
    sys.setdefaultencoding('UTF8')
    make_paragraphs()







