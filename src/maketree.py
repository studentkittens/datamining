#!/usr/bin/env python
# encoding: utf-8


from itertools import permutations


class Document:
    def __init__(self, text):
        self._text = text


class ClusterNode:
    def __init__(self, doc, left=None, right=None):
        self._doc = doc
        self._left = left
        self._right = right
    def __repr__(self):
        return "..."


class ClusterTuple:
    def __init__(self, distance, a, b):
        self._a = a
        self._b = b
        self._distance = distance

    def __gt__(self, node):
        return self._distance > node._distance

    def __lt__(self, node):
        return self._distance < node._distance

    def __ge__(self, node):
        return self._distance >= node._distance

    def __le__(self, node):
        return self._distance <= node._distance

    def __eq__(self, node):
        return self._distance == node._distance

    def __hash__(self):
        return sum([hash(self._distance), id(a), id(b)])

    def __repr__(self):
        return "({d} [{a}-{b}])".format(d=self._distance, a=self._a, b=self._b)

if __name__ == '__main__':
    docs = [Document("A"), Document("B"), Document("C")]



    a = ClusterNode(docs[0])
    b = ClusterNode(docs[1])
    c = ClusterNode(docs[2])

    s = set()
    i = 0
    for a, b in permutations([a, b, c], 2):
        s.add(ClusterTuple(i, a, b))
        i += 1

    print(s)
