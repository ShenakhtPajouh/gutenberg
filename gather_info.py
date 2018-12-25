from gutenberg.query import get_metadata
import re


def isvalid(id_num):
    """

    Check if a gutenberg book is an english textbook.

    Args:
        id_num: id of gutenberg book.

    Returns:
        a boolean which shows if id_num is id of an english text book

    """
    try:
        language = get_metadata('language', id_num)
        form = get_metadata('formaturi', id_num)
        if 'en' not in language:
            return False
        form = ' '.join(form)
        if re.search(r'\d+\.txt', form):
            return True
        return False
    except:
        return False



def find_books_html(text):
    """

    Gather all books ids which are linked in a web page.

    Args:
        text: raw-text of a web page

    Returns:
        a list of integers which is all id of books find in that page

    """
    links = re.findall(r'<https://www.gutenberg.org/ebooks/.*>', text)
    links = ' '.join(links)
    ids = re.findall(r'\d+', links)
    ids = [int(x) for x in ids]
    return ids











