#!/usr/bin/env python
# encoding: utf-8

import os
import glob
import Stemmer


def get_stopwords():
    return "ist ein sein je der desto es viel zum die von".split()


def read_document(path):
    with open(path, 'r') as f:
        doc = f.read()
    return doc


def read_directory(root, pattern='*.txt'):
    'Read a the text of a single director into a list'
    result = []
    for path in glob.glob(os.path.join(root, pattern)):
        result.append(read_document(path))
    return result


def sanitize_word(word):
    'Normalize a single word'
    return ''.join(filter(str.isalnum, word)).lower()


def doc_to_words(doc, stopwords):
    '''
    :doc: The text as newline seperated string
    :stopwords: List of words to filter (after normalization)
    :returns: a list of words in the document without the stopwords
    '''
    stemmer = Stemmer.Stemmer('german')
    words = []
    for line in doc.splitlines():
        for word in line.split():
            good_word = sanitize_word(word)
            if good_word not in stopwords:
                words.append(good_word)

    return stemmer.stemWords(words)

if __name__ == '__main__':
    import sys
    for document in read_directory(sys.argv[1]):
        print(doc_to_words(document, get_stopwords()))
