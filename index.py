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
        self.forward_index[current_id] = parsed_text
        for position, word in enumerate(parsed_text): 
            # TODO: defaultdict
            if word not in self.inverted_index:
                self.inverted_index[word] = []
            self.inverted_index[word].append((position, current_id))


    def save_on_disk(self, index_dir):
        inverted_index_file_name = os.path.join(index_dir, "inverted_index")
        forward_index_file_name  = os.path.join(index_dir, "forward_index")
        url_to_id_file_name      = os.path.join(index_dir, "url_to_id")

        inverted_index_file = open(inverted_index_file_name, 'w')
        forward_index_file  = open(forward_index_file_name, 'w')
        url_to_id_file      = open(url_to_id_file_name, 'w')

        json.dump(self.inverted_index, inverted_index_file)
        json.dump(self.forward_index, forward_index_file)
        json.dump(self.url_to_id, url_to_id_file)


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


