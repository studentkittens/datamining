#!/usr/bin/env python
# encoding: utf-8


# Drawing with graphviz
import pydot as dot


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

    def __lt__(self, node):
        return self.dist < node.dist

    def __eq__(self, node):
        return (self.a is node.a or self.a is node.b) and (self.b is node.a or self.b is node.b)

    def __hash__(self):
        return id(a) + id(b)

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

    s = list()

    a, b, c, d, e = cluster
    s.append(Distance(2, a, b))
    s.append(Distance(4, a, c))
    s.append(Distance(5, a, d))
    s.append(Distance(7, a, e))

    s.append(Distance(3, b, c))
    s.append(Distance(6, b, d))
    s.append(Distance(8, b, e))

    s.append(Distance(1, c, d))
    s.append(Distance(2, c, e))

    s.append(Distance(1, d, e))

    # Initial sort
    s.sort(reverse=True)

    # Iterate till n-1 new nodes have been created.
    for i in range(len(cluster) - 1):
        # Get the cluster with the shortest distance out
        # On every iteration the length should be sum(0..n-1)
        print('len(s) = ', len(s), s, end='')

        nearest = s.pop()
        left, right = nearest.a, nearest.b

        # Create a new cluster, containing both
        parent = Cluster(left.docs + right.docs,
                left=left, right=right,
                name=''.join((left.name, right.name))
        )

        print(' ->', left.name + "-" + right.name)

        for dist in s:
            if dist.a is left or dist.a is right:
                dist.a = parent
            elif dist.b is left or dist.b is right:
                dist.b = parent

        # Remember to draw the edge
        graph.add_edge(dot.Edge(parent.name, left.name))
        graph.add_edge(dot.Edge(parent.name, right.name))

        # Not exactly sure if this is needed
        s = sorted(set(s), reverse=True)

    graph.write_png('cluster.png')

    print("Left in set: ", len(s))
    print("Docs:", ' '.join([doc.text for doc in parent.docs]))
