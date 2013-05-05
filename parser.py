#!/usr/bin/env python
# encoding: utf-8
import sys
import os
import numpy


STOP = ['die', 'von', 'ist', 'es', 'zum', 'viele', 'je', 'der', 'desto', 'ein']
V = ['vertrag', 'riskant', 'weg', 'profit', 'rechtfertigung']


def read_doc(path):
    doc = ''
    with open(path, 'r') as f:
        doc = f.read()
    return doc


def get_f(docs):
    f = numpy.zeros((len(docs), len(V)))
    for r, doc in enumerate(docs):
        for i, v in enumerate(V):
            f[r, i] = doc.lower().count(v)
    return f


def get_vd(f):
    vd = numpy.array(f)
    for i, x in numpy.ndenumerate(vd):
        vd[i] = min(x, 1)
    return vd


def get_v_max(f):
    v_max = numpy.zeros(f.shape[1])
    cols = f.shape[1]
    for col in range(cols):
        v_max[col] = max(f[:, col])
    return v_max


def get_df(f):
    v_max = numpy.zeros(f.shape[1])
    cols = f.shape[1]
    for col in range(cols):
        v_max[col] = sum(f[:, col])
    return v_max


def get_idf(N, df):
    return numpy.log10(N / df)


def get_tf_idf(nf, idf):
    tf_idf = numpy.zeros(nf.shape)
    for idx, row in enumerate(nf):
        tf_idf[idx] = row * idf

    return tf_idf


def get_nf(f, v_max):
    nf = numpy.zeros(f.shape)
    for i, r in enumerate(f):
        nf[i] = f[i] / v_max
    return nf


def read_dir(root):
    result = []
    for path in os.listdir(root):
        result.append(read_doc(os.path.join(root, path)))
    return result


def count_words(doc):
    counts = {}
    for line in doc.splitlines():
        for word in line.split():
            good_word = sanitize(word)
            if good_word in counts:
                counts[good_word] += 1
            else:

                counts[good_word] = 1
    return counts


def sanitize(word):
    return ''.join(filter(str.isalnum, word)).lower()


def sort_counts(counts):
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)

if __name__ == '__main__':
    docs = read_dir(sys.argv[1])
    #one_string = "\n".join(docs)
    #counts = sort_counts(count_words(one_string))

#    for k, v in counts:
        #print(k, v)
#    f_list = [get_f(doc.lower()) for doc in docs]
    f = get_f(docs) # textfrequency
    print("f\n", f)
    vd = get_vd(f)
    print('vd\n', vd)
    v_max = get_v_max(f)
    print('v_max\n', v_max)
    nf = get_nf(f, v_max)
    print('nf\n', nf)
    df = get_df(f)
    print('df\n', df)
    idf = get_idf(len(docs), df)
    print('idf\n', idf)
    tf_idf = get_tf_idf(nf, idf)
    print('tf_idf\n', tf_idf)
    #pp.pprint(f_list)
