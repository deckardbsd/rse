from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import sent_tokenize, TreebankWordTokenizer
import itertools
import string


def stem_and_tokenize(text):
    sents = sent_tokenize(text)
    tokens = list(itertools.chain(*[TreebankWordTokenizer().tokenize(sent) for sent in sents]))
    print 'tokens --- ', tokens
    stems = [PorterStemmer().stem(token) for token in tokens]
    print 'stems --- ', stems
    # terms = [stem.lower() for stem in stems if stem not in string.punctuation]
    terms = [stem for stem in stems if stem not in string.punctuation]
    return terms


def query_terms(query_raw):
    return stem_and_tokenize(query_raw)


def doc_terms(doc_raw):
    return stem_and_tokenize(doc_raw)




    
