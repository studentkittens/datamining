#!/usr/bin/env python
# encoding: utf-8


import numpy as np

from vocabular import sanitize_word


def termfreq(docs, voc):
    '''
    Matrix with docs on columns, words on rows. Value is the count of word.
    '''
    f = np.zeros((len(docs), len(voc)))
    for r, doc in enumerate(docs):
        for i, v in enumerate(voc):
            f[r, i] = doc.count_voc(v)
    return f


def bag_of_words(freq):
    '''
    0/1 Matrix with docs on columns, words on rows.
    '''
    vd = np.array(freq)
    for i in range(freq.shape[0]):
        for j in range(freq.shape[1]):
            vd[i, j] = 1 if freq[i, j] else 0
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


def inverse_doc_freq(N, bag_of_words):
    '''
    :N: Number of Documents
    :df: document_freq
    '''
    n_docs = np.zeros(bag_of_words.shape[1])
    for row in bag_of_words:
        n_docs += row

    return np.log10(N / n_docs)


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


def weight_matrix(norm_freq, inverse_doc_freq):
    return norm_freq * inverse_doc_freq


def document_abs(weight_matrix):
    abs_vec = np.zeros(weight_matrix.shape[0])
    for idx, row in enumerate(weight_matrix):
        abs_vec[idx] = np.linalg.norm(row)

    return abs_vec


def distance(weight_a, weight_b, abs_a, abs_b):
    return np.dot(weight_a, weight_b) / (abs_a * abs_b)
