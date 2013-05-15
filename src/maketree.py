#!/usr/bin/env python
# encoding: utf-8

import pydot as dot


from cluster import ClusterLeaf, ClusterTree
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


def draw_graphviz(root):
    graph = dot.Dot(graph_type='digraph')
    graph.set_node_defaults(shape='circle', fixedsize='true',
            height=.85, width=.85, fontsize=10
    )

    def traverse(node, parent=None):
        if not node is None:
            gvnode = dot.Node(name=node.name, label=node.label)
            graph.add_node(gvnode)
            if not parent is None:
                graph.add_edge(dot.Edge(parent, node.name))
            traverse(node.left, gvnode)
            traverse(node.right, gvnode)

    traverse(root)
    graph.write_png("cluster.png")


def maketree(dists, clusterLeafs):

    # sort dists
    dists = sorted(dists, key=lambda a: a.dist, reverse=True)
    nDocs = len(clusterLeafs)

    for dist in dists:
        # algo is finished if cluster root contains all documents
        if not clusterLeafs[0].root.nLeafs < nDocs:
            break

        if not dist.a.root is dist.b.root:
            # link previous root nodes under new root node
            parent = ClusterTree(dist.a.root, dist.b.root, dist.a.root.docs + dist.b.root.docs)

        #else:
            # leaf1 and leaf2 are already in the same cluster, so pass

    #clusterLeaf[x].root is now all the same
    #draw_graphviz(clusterLeafs[0].root)
    return clusterLeafs[0].root
