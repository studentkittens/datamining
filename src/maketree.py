#!/usr/bin/env python
# encoding: utf-8


import pydot as dot
from itertools import permutations


class Document:
    def __init__(self, text):
        self.text = text


class Cluster:
    def __init__(self, docs, left=None, right=None, name=''):
        self.docs = docs
        self.left = left
        self.right = right
        self.name = name

    def __repr__(self):
        return self.name


class Distance:
    def __init__(self, dist, a, b):
        self.a = a
        self.b = b
        self.dist = dist

    def __gt__(self, node):
        return self.dist > node.dist

    def __lt__(self, node):
        return self.dist < node.dist

    def __ge__(self, node):
        return self.dist >= node.dist

    def __le__(self, node):
        return self.dist <= node.dist

    def __eq__(self, node):
        return self.dist == node.dist

    def __hash__(self):
        return id(a) + id(b) + self.dist

    def __repr__(self):
        return "Dist({a}-{b}={d})".format(d=self.dist, a=self.a, b=self.b)


if __name__ == '__main__':
    graph = dot.Dot(graph_type='digraph')
    docs = [
            Document("Hans"),
            Document("stohl"),
            Document("die"),
            Document("Gans"),
            Document("!")
    ]

    cluster = [
            Cluster([docs[0]], name="A"),
            Cluster([docs[1]], name="B"),
            Cluster([docs[2]], name="C"),
            Cluster([docs[3]], name="D"),
            Cluster([docs[4]], name="E")
    ]

    s = set()
    a, b, c, d, e = cluster
    s.add(Distance(2, a, b))
    s.add(Distance(4, a, c))
    s.add(Distance(5, a, d))
    s.add(Distance(7, a, e))

    s.add(Distance(3, b, c))
    s.add(Distance(6, b, d))
    s.add(Distance(8, b, e))

    s.add(Distance(1, c, d))
    s.add(Distance(2, c, e))

    s.add(Distance(1, d, e))

    print(len(s))

    # Iterate till n-1 new nodes have been created.
    for i in range(len(cluster) - 1):
        # Get the cluster with the shortest distance out
        print(s, end='')
        nearest = s.pop()
        left, right = nearest.a, nearest.b

        # Create a new cluster, containing both
        parent = Cluster(left.docs + right.docs,
                left=left, right=right,
                name=''.join((left.name, right.name))
        )

        print(' ->', parent.name)

        # Update set with the new parent node
        for dist in s:
            # Set a to parent if it is in there
            if dist.a is left or dist.a is right:
                dist.a = parent
            # Otherwise search dist.b
            elif dist.b is left or dist.b is right:
                dist.b = parent
            # elsewhise leave it as it is.

        # Remember to draw the edge
        graph.add_edge(dot.Edge(parent.name, left.name))
        graph.add_edge(dot.Edge(parent.name, right.name))

        # Not entirely sure if this is needed
        s = set(list(s))

    graph.write_png('cluster.png')

    print("Left in set: ", len(s))
    print("Docs:", ' '.join([doc.text for doc in parent.docs]))
