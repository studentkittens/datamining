#!/usr/bin/env python
# encoding: utf-8


import numpy as np


def textfrequency(docs):
    f = np.zeros((len(docs), len(V)))
    for r, doc in enumerate(docs):
        for i, v in enumerate(V):
            f[r, i] = doc.lower().count(v)
    return f


def get_vd(f):
    vd = np.array(f)
    for i, x in np.ndenumerate(vd):
        vd[i] = min(x, 1)
    return vd


def get_v_max(f):
    v_max = np.zeros(f.shape[1])
    cols = f.shape[1]
    for col in range(cols):
        v_max[col] = max(f[:, col])
    return v_max


def get_df(f):
    v_max = np.zeros(f.shape[1])
    cols = f.shape[1]
    for col in range(cols):
        v_max[col] = sum(f[:, col])
    return v_max


def get_idf(N, df):
    return np.log10(N / df)


def get_tf_idf(nf, idf):
    tf_idf = np.zeros(nf.shape)
    for idx, row in enumerate(nf):
        tf_idf[idx] = row * idf

    return tf_idf


def get_nf(f, v_max):
    nf = np.zeros(f.shape)
    for i, r in enumerate(f):
        nf[i] = f[i] / v_max
    return nf

