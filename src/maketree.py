#!/usr/bin/env python
# encoding: utf-8

from cluster import Cluster
from document import Document
from timing import timing
import calculations as calc

class Distance:
    def __init__(self, dist, a, b):
        self.a = a
        self.b = b
        self.dist = dist

    def __lt__(self, node):
        return self.dist < node.dist

    def __eq__(self, node):
        #print("eq")
        return (self.a is node.a or self.a is node.b) and (self.b is node.a or self.b is node.b)

    def __hash__(self):
        #print("Hassh?")
        return id(self.a) + id(self.b)

    def __repr__(self):
        return "Dist({a}-{b}={d})".format(d=self.dist, a=self.a, b=self.b)

def build_cluster_tree(
        docs, weight_matrix,
        document_abs, norm_termfreq, termfreq,
        vocabular):
    n_rows = weight_matrix.shape[0]

    with timing('Preparing distances'):
        distances = []
        clusters = []
        for doc in docs:
            clusters.append(Cluster([doc]))

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
                distances.append(Distance(dist, clusters[i], clusters[j]))

                doc.distances[docs[j].name] = dist
                docs[j].distances[doc.name] = dist

    with timing('Calling maketree'):
        return maketree(distances, len(clusters))


def maketree(distances, cluster_len):
    s = distances

    # parent is the topmost node
    parent = None

    # Iterate till n-1 new nodes have been created.
    for i in range(cluster_len - 1):
        # Get the cluster with the shortest distance out
        # On every iteration the length should be sum(0..n-1)
        nearest = max(s)
        for idx, elem in enumerate(s):
            if elem is nearest:
                del s[idx]
                break

        left, right = nearest.a, nearest.b

        # Create a new cluster, containing both
        parent = Cluster(left.docs + right.docs,
                left=left, right=right
        )

        for dist in s:
            if dist.a is left or dist.a is right:
                dist.a = parent
            elif dist.b is left or dist.b is right:
                dist.b = parent

        s = list(frozenset(s))

    return parent

