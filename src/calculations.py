#!/usr/bin/env python
# encoding: utf-8


import numpy as np


def termfreq(docs):
    '''
    Matrix with docs on columns, words on rows. Value is the count of word.
    '''
    f = np.zeros((len(docs), len(V)))
    for r, doc in enumerate(docs):
        for i, v in enumerate(V):
            f[r, i] = doc.lower().count(v)
    return f


def bag_of_words(freq):
    '''
    0/1 Matrix with docs on columns, words on rows.
    '''
    vd = np.array(freq)
    for i, x in np.ndenumerate(vd):
        vd[i] = min(x, 1)
    return vd


def max_per_doc(freq):
    '''
    Returns a vector with the max occurence of a word on all documents.
    '''
    v_max = np.zeros(freq.shape[1])
    cols = freq.shape[1]
    for col in range(cols):
        v_max[col] = max(freq[:, col])
    return v_max


def doc_freq(freq):
    '''
    Vector in which the word[i] appears.
    '''
    v_max = np.zeros(freq.shape[1])
    cols = freq.shape[1]
    for col in range(cols):
        v_max[col] = sum(freq[:, col])
    return v_max


def inverse_doc_freq(N, doc_freq):
    '''
    :N: Number of Documents
    :df: document_freq
    '''
    return np.log10(N / doc_freq)


def term_freq_to_inverse_doc_freq(nf, idf):
    '''
    Yes, srsly.
    '''
    tf_idf = np.zeros(nf.shape)
    for idx, row in enumerate(nf):
        tf_idf[idx] = row * idf

    return tf_idf


def normalized_term_freq(freq, v_max):
    nf = np.zeros(freq.shape)
    for idx, row in enumerate(freq):
        nf[idx] = freq[idx] / v_max
    return nf
