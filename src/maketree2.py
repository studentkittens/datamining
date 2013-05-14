#!/usr/bin/env python
# encoding: utf-8

from cluster2 import *
from document import Document
from timing import timing

import calculations as calc

class Distance:
    def __init__(self, dist, a, b):
        self.a = a
        self.b = b
        self.dist = dist
    def __repr__(self):
      return '(%f, %s - %s)' % (self.dist, str(self.a), str(self.b))

def build_cluster_tree(
        docs, weight_matrix,
        document_abs, norm_termfreq, termfreq,
        vocabular):
    with timing('Preparing distances'):
        distances = []
        n_rows = len(docs)

        #build bottom of cluster tree
        clusterLeafs = [ClusterLeaf(doc) for doc in docs]

        sorted_mapping = {voc: idx for idx, voc in enumerate(vocabular)}

        for i in range(n_rows):
            doc = docs[i]
            doc.distances[doc.name] = 1.0
            doc.set_norm_freq(termfreq[i], norm_termfreq[i], sorted_mapping)

            for j in range(i + 1, n_rows):
                dist = calc.distance(
                        weight_matrix[i], weight_matrix[j],
                        document_abs[i], document_abs[j]
                )
                distances.append(Distance(dist, clusterLeafs[i], clusterLeafs[j]))

                doc.distances[docs[j].name] = dist
                docs[j].distances[doc.name] = dist

    with timing('Calling maketree'):
        return maketree(distances, clusterLeafs)

def maketree(dists, clusterLeafs):
    # sort dists
    dists = sorted(dists, key = lambda a : a.dist)
    # index to last element in distance list
    i = len(dists) - 1
    nDocs = len(clusterLeafs)
    # algo is finished if cluster root contains all documents
    while clusterLeafs[0].root.nLeafs < nDocs:
      assert(i >= 0)
      dist = dists[i]
      if not dist.a.root is dist.b.root:
        #link previous root nodes under new root node
        ClusterTree(dist.a.root, dist.b.root, dist.a.root.docs + dist.b.root.docs)
      #else: leaf1 and leaf2 are already in the same cluster, so pass
      i -= 1
    #clusterLeaf[x].root is now all the same
    return clusterLeafs[0].root
