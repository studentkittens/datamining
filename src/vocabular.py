#!/usr/bin/env python
# encoding: utf-8

import os
import glob
import codecs

import Stemmer

from document import Document

stemmer = Stemmer.Stemmer('german')


def get_stopwords():
    return "ist ein sein je der desto es viel zum die von".split()


def read_document(path):
    with codecs.open(path, 'r', 'utf-8') as f:
        text = f.read()
        doc = Document(path, text, text_to_words(text, get_stopwords()))
    return doc


def read_directory(root, pattern='*.txt'):
    'Read a the text of a single director into a list'
    result = []
    for path in sorted(glob.glob(os.path.join(root, pattern))):
        print(path.ljust(50, ' '), end='\r')
        result.append(read_document(path))
    print()
    return result


def sanitize_word(word):
    'Normalize a single word'
    return stemmer.stemWord(''.join(filter(str.isalnum, word)).lower())


def text_to_words(doc, stopwords):
    '''
    :doc: The text as newline seperated string
    :stopwords: List of words to filter (after normalization)
    :returns: a list of words in the document without the stopwords
    '''
    words = []
    for line in doc.splitlines():
        for word in line.split():
            good_word = sanitize_word(word)
            if good_word not in stopwords:
                words.append(good_word)

    return words

if __name__ == '__main__':
    import sys
    for document in read_directory(sys.argv[1]):
        print(document.text, document.vocs)
