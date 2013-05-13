from maketree2 import *
from cluster2 import *

class Doc:
  def __init__(self,name): self.name = name

def printTraverse(tree, indent=0):
  if tree:
    print(' >'*indent, tree)
    indent += 1
    printTraverse(tree.left, indent)
    printTraverse(tree.right, indent)

print('test treenodes') 
docs = [Doc('d1'), Doc('d2'), Doc('d3')]
leafs = [ClusterLeaf(doc) for doc in docs]

for node in leafs:
  print('name:', node, 'nLeafs:',node.nLeafs, 'left:', node.left, 'right',node.right)

t1 = ClusterTree(leafs[0], leafs[1])
t2 = ClusterTree(t1, leafs[2])

treenodes = [t1, t2]
for node in treenodes:
  print('name:', node, 'nLeafs:',node.nLeafs, 'left:', node.left, 'right',node.right)

printTraverse(t2)


print('test maketree') 
dists = [
    Distance(.9, leafs[0], leafs[1]),
    Distance(.1, leafs[0], leafs[2]),
    Distance(.5, leafs[1], leafs[2])
]

tree = maketree(dists, leafs)
printTraverse(tree)







