import nltk
from paragraph import Paragraph
from HP import Tags
import re


def tokenize(par):
    """

    Args:
        par: a string

    Returns:
        a list of lists of strings which tokenize par to sentences and words.

    """
    text = nltk.tokenize.sent_tokenize(par)
    text = [nltk.tokenize.word_tokenize(sent) for sent in text]
    return text


def tagger(par):
    """

    Args:
        par: either a Paragraph or list of lists wich each list is a list of words (for a sentence)

    Returns:
          a set of tags (int)
    """
    if isinstance(par, Paragraph):
        par = par.text()
    tags = []
    tokens = sum(par, [])
    text = " ".join(tokens)
    words = [word for word in tokens if re.search(r'\w', word)]
    if len(words) < 16:
        tags.append(Tags.NOT_PARAGRAPH)
    else:
        tags.append(Tags.PARAGRAPH)
    if len(par) < 4 and len(words) < 150:
        tags.append(Tags.SHORT)
    elif len(words) < 250:
        tags.append(Tags.MEDIUM)
    elif len(words) < 500:
        tags.append(Tags.LONG)
    else:
        tags.append(Tags.TOO_LONG)

    if re.search(r'``.+\'\'', text) is None:
        tags.append(Tags.WITHOUT_DIALOGUE)
    if tokens[0] == '``' and tokens[-1] == "''" and ("``" not in tokens[1:-1] or "''" not in tokens[1:-1]):
        tags.append(Tags.WHOLE_DIALOGUE)
    return set(tags)







