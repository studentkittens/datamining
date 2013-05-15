#!/usr/bin/env python
# encoding: utf-8
cimport cython


import numpy as np

cimport numpy as np
DTYPE = np.int
# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.int_t DTYPE_t


@cython.boundscheck(False)
def termfreq(object docs, object voc):
    cdef int doc_len = len(docs)
    cdef int voc_len = len(voc)

    cdef int i = 0
    cdef int r = 0


    cdef np.ndarray[DTYPE_t, ndim=2] term_freq = np.zeros([doc_len, voc_len], dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] bag_of_words = np.zeros([doc_len, voc_len], dtype=DTYPE)

    for r in range(doc_len):
        for i in range(voc_len):
            count = docs[r].count_voc(voc[i])
            term_freq[r, i] = count
            bag_of_words[r, i] = 1 if count else 0

            i += 1
        r += 1

    #for r, doc in enumerate(docs):
    #    for i, v in enumerate(voc):
    #        count = doc.count_voc(v)
    #        term_freq[r, i] = count
    #        bag_of_words[r, i] = 1 if count else 0

    return term_freq, bag_of_words


def max_per_doc(freq):
    '''
    Returns a vector with the max occurence of a word on all documents.
    '''
    v_max = np.zeros(freq.shape[1])
    cols = freq.shape[1]
    for col in range(cols):
        v_max[col] = max(freq[:, col])
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
