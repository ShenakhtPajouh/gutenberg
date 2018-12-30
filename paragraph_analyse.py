import nltk
from paragraph import Paragraph

def tokenize(par):
    text = nltk.tokenize.sent_tokenize(par)
    text = [nltk.tokenize.word_tokenize(sent) for sent in text]
    return text

def tagger(par):
    if isinstance(par, Paragraph):
        par = Paragraph.text

