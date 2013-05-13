#!/usr/bin/env python
# encoding: utf-8


class ClusterNode:
    def __init__(self): 
      self.name = 'abstract ClusterNode'
    def __repr__(self):
        return self.name
    @property
    def left(self): 
      return None
    @property
    def right(self): 
      return None

class ClusterTree(ClusterNode):
    def __init__(self, left, right):
        self._left = left
        self._right = right
        self.name = left.name + ' ' + right.name
        # nLeafs counts number of leaf nodes in tree
        # maketree alg terminates if nLeafs is count of documents
        self.nLeafs = left.nLeafs + right.nLeafs
        # update root in subtrees
        left.setRoot(self)
        right.setRoot(self)
    def setRoot(self, root):
      self.left.setRoot(root)
      self.right.setRoot(root)
    @property
    def left(self): 
      return self._left
    @property
    def right(self): 
      return self._right
  

class ClusterLeaf(ClusterNode):
  def __init__(self, doc):
    self.doc = doc
    # root of cluster tree for fast look up
    # initially root is self, since every document has its own cluster
    self.root = self
    self.name = doc.name
    self.nLeafs = 1
  def setRoot(self, root):
    self.root = root


