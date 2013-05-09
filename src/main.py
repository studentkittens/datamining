#!/usr/bin/env python
# encoding: utf-8


import calculations as calc
import vocabular as voc

import sys
import numpy as np

from maketree import Distance, maketree
from cluster import Cluster
from gui import show_treevis

if __name__ == '__main__':
    docs = voc.read_directory(sys.argv[1])

    vocabular = []
    for doc in docs:
        vocabular += doc.vocs

    vocabular = list(set(vocabular))

    termfreq = calc.termfreq(docs, vocabular)
    bag_of_words = calc.bag_of_words(termfreq)
    v_max = calc.max_per_doc(termfreq)
    norm_termfreq = calc.normalized_term_freq(termfreq, v_max)
    inverse_doc_freq = calc.inverse_doc_freq(len(docs), bag_of_words)
    weight_matrix = calc.weight_matrix(norm_termfreq, inverse_doc_freq)
    document_abs = calc.document_abs(weight_matrix)

    print("Full vocabulary\n", vocabular)
    print("Termfreq\n", termfreq)
    print("Bag of Words\n", bag_of_words)
    print("v_max\n", v_max)
    print("Normed Termfreq\n", norm_termfreq)
    print("Inverse Doc Freq\n", inverse_doc_freq)
    print("Weight Vec:\n", weight_matrix)
    print("Document Abs:\n", document_abs)

    np.set_printoptions(precision=16)

    n_rows = weight_matrix.shape[0]

    distances = []
    clusters = []
    for doc in docs:
        clusters.append(Cluster([doc]))

    for i in range(n_rows):
        doc = docs[i]
        doc.distances[doc.name] = 1.0
        for j in range(i + 1, n_rows):
            dist = calc.distance(weight_matrix[i], weight_matrix[j], document_abs[i], document_abs[j])
            distances.append(Distance(dist, clusters[i], clusters[j]))

            doc.distances[docs[j].name] = dist
            docs[j].distances[doc.name] = dist
        print(doc, doc.distances)

    print(distances)

    tree = maketree(distances, len(clusters))
    show_treevis(tree)
