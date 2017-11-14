# two main types of indexes

# -> forward index
# -> inverted index


# Forward Index - collection of parsed documents
## a map of documents to words
# ---
# doc1 -> [ learning, python, how, to ] 
# doc2 -> [ learning, C++ ]
# doc3 -> [ python, C++ ]


# Inverted Index
## a map of words to documents
## For large collections is fast.
# ---
# learning -> [doc1, doc2 ]
# python -> [ doc1, doc3 ]
# how -> [ doc1 ]
# to -> [ doc1 ]
# C++ -> [ doc2, doc3 ]


# query: [ learning, python ]

# TODO: improve this
# Indexer assumets that collection fits in memory (RAM)
## create minima and then expand
import argparse
import base64
import json
import os

from utils import *


class Indexer(object):
    def __init__(self):
        self.inverted_index = dict()
        self.forward_index  = dict()
        self.url_to_id      = dict()
        self.doc_count      = 0

    # TODO: remove this assumptions
    # assumes that add_document() is never called twice for a document
    # assumes that a document has an unique url
    # parsed_text is a list of words
    def add_document(self, url, parsed_text):
        self.doc_count += 1
        assert url not in self.url_to_id
        current_id = self.doc_count 
        self.url_to_id[url] = current_id
        self.forward_index[current_id] = parsed_text
        for position, word in enumerate(parsed_text): 
            # TODO: defaultdict
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            self.inverted_index[word].append((position, current_id))


    def save_on_disk(self, index_dir):
        ''' save the index in a file on disk '''
        def dump_to_file(source, fname):
            file_path = os.path.join(index_dir, fname)
            with open(file_path, 'wb') as myf:
                json.dump(source, myf, indent=3)

        dump_to_file(self.inverted_index, "inverted_index")
        dump_to_file(self.forward_index, "forward_index")
        dump_to_file(self.url_to_id, "url_to_id")


class Searcher(object):
    def __init__(self, index_dir):
        self.inverted_index = dict()
        self.forward_index = dict()
        self.url_to_id = dict()
        self.id_to_url = dict()

        def load_from_file(fname):
            file_path = os.path.join(index_dir, fname)
            with open(file_path, 'rb') as myf:
                dst = json.load(myf)
                return dst

        self.inverted_index = load_from_file("inverted_index")
        self.forward_index = load_from_file("forward_index")
        self.url_to_id = load_from_file("url_to_id")

        self.id_to_url = {v: k for k,v in self.url_to_id.iteritems()}

    def find_documents(self, words):
        return sum((self.inverted_index[word] for word in words), [])

    def get_url(self, id):
        return self.id_to_url[id]


def create_index_from_dir(stored_documents_dir, index_dir):
    indexer = Indexer()
    for f in os.listdir(stored_documents_dir):
        with open(os.path.join(stored_documents_dir, f)) as opened_fn:
            # TODO: words are not just separated by space
            parsed_doc = parseRedditPost(opened_fn.read()).split(' ')
            indexer.add_document(base64.b16decode(f), parsed_doc)
    indexer.save_on_disk(index_dir)


def main():
    parser = argparse.ArgumentParser(description='Index /r/learnprogramming')
    parser.add_argument('--stored_documents_dir', dest='stored_documents_dir')
    parser.add_argument('--index_dir', dest='index_dir')
    args = parser.parse_args()
    create_index_from_dir(args.stored_documents_dir, args.index_dir)


if __name__== '__main__':
    main()


