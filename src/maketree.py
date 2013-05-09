#!/usr/bin/env python
# encoding: utf-8

from cluster import Cluster
from document import Document


class Distance:
    def __init__(self, dist, a, b):
        self.a = a
        self.b = b
        self.dist = dist

    def __lt__(self, node):
        return self.dist < node.dist

    def __eq__(self, node):
        return (self.a is node.a or self.a is node.b) and (self.b is node.a or self.b is node.b)

    def __hash__(self):
        return id(self.a) + id(self.b)

    def __repr__(self):
        return "Dist({a}-{b}={d})".format(d=self.dist, a=self.a, b=self.b)


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

        s = list(set(s))

    return parent
