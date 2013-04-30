#!/usr/bin/env python
# encoding: utf-8


from cluster import Cluster
from document import Document


LOREM = ''' Eget. Dolor est cursus primis fames semper vestibulum. Nibh arcu, neque fusce, nam habitasse. Pulvinar. Elit fusce sodales mollis ve cras pede. Tellus odio dis viverra dis, mi ipsum. Arcu pulvinar class ad urna turpis rhoncus in, nunc. Magnis fusce arcu aenean porttitor mi, donec pellentesque accumsan velit sollicitudin, penatibus dictum ut diam. Ante litora hendrerit. Quam quis leo. Quam magna eu orci. Ante a elit risus. Viverra, nisl pulvinar ut, nisl inceptos. Pede sociis augue dictum malesuada. Placerat tempor quam erat mollis, litora ad. Montes ipsum blandit rutrum dolor primis fames enim scelerisque at, nostra ad augue. Etiam iaculis id, iaculis id, velit pharetra. Ve ornare. Dignissim massa ut fames ac mi erat odio fusce eros eu consectetuer commodo.
Tincidunt id, imperdiet adipiscing, conubia orci in sollicitudin aptent, congue, fames. Malesuada justo eu fermentum posuere, tempus ridiculus ad, in odio. Sociis odio ad. Augue eget netus, eu nam duis class lacus, sapien hendrerit volutpat, id ligula. Hendrerit faucibus montes aptent hendrerit ve, turpis. Nibh torquent eu, ullamcorper ad, aptent. Enim orci duis. Nisi vivamus sodales nonummy ornare nulla parturient ve, lobortis. Porta magnis sagittis malesuada ac, nullam conubia semper nibh dictum. Ad, venenatis nulla, venenatis volutpat quis nullam facilisi neque eni pede, leo. Elit tortor adipiscing vitae urna, ac sollicitudin turpis risus. Duis ipsum hymenaeos. Vehicula ad condimentum orci, curabitur dui, blandit et, eu lorem vulputate maecenas ad condimentum pede. Ve condimentum pede, nisl, pharetra a, maecenas. At amet, ornare tristique mi, in mattis consectetuer dapibus.
Morbi vulputate. Libero. Purus volutpat parturient imperdiet. Elit erat, dui dolor varius euismod mauris. Sit pede sed nulla purus, dis. Mus nulla neque, sociosqu massa dui netus porttitor vehicula. Imperdiet netus sit donec nam lobortis consequat at amet metus ornare quam. Consectetuer potenti vitae eu habitasse nulla. Posuere interdum. Cras, rhoncus odio, ad donec ad consequat condimentum, class consequat neque ante. Molestie, penatibus porta ultricies habitant. Tempus ac sit convallis purus nisi vitae rhoncus nonummy. Cras lorem facilisis lobortis porta venenatis cubilia nunc. Lacus tempus fusce donec. Cursus varius massa id non porttitor aenean dui lectus proin vestibulum. Curae, duis urna.
Mattis. Sapien, non ante pharetra conubia nascetur mi. Dis nibh elit hymenaeos mauris nascetur neque nulla aliquet sagittis enim mauris non. Pretium tempor etiam sociis litora massa per diam parturient semper in eros turpis leo mollis laoreet. Dolor justo nec parturient venenatis, diam rhoncus curae magna fermentum. Habitasse, lorem imperdiet nulla venenatis ac. Habitant, erat rhoncus eget, et quam. Massa cursus ac accumsan nec, risus. Placerat ad sit montes ut. Arcu. Metus scelerisque vehicula aliquam erat urna dui. At, vitae pharetra per. At. Sociis a, praesent quam tellus ac ligula mi, praesent amet imperdiet eleifend. Quis. Facilisi nisi cras ultricies pellentesque. Magnis maecenas consequat fusce nisl dictum, ve cras ipsum praesent, penatibus.
'''


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


def maketree():
    docs = [
            Document('hans_der_pole.txt', LOREM),
            Document('stohl_nachts.txt', LOREM),
            Document('die.txt', LOREM),
            Document('weiße_ganz.txt', LOREM),
            Document('ausrufezeichen.txt', LOREM)
    ]

    cluster = [
            Cluster([docs[0]], name="A"),
            Cluster([docs[1]], name="B"),
            Cluster([docs[2]], name="C"),
            Cluster([docs[3]], name="D"),
            Cluster([docs[4]], name="E")
    ]

    s = []

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

    # parent is the topmost node
    parent = None

    # Iterate till n-1 new nodes have been created.
    for i in range(len(cluster) - 1):
        # Get the cluster with the shortest distance out
        # On every iteration the length should be sum(0..n-1)
        nearest = s.pop()
        left, right = nearest.a, nearest.b

        # Create a new cluster, containing both
        parent = Cluster(left.docs + right.docs,
                left=left, right=right,
                name=''.join((left.name, right.name))
        )

        for dist in s:
            if dist.a is left or dist.a is right:
                dist.a = parent
            elif dist.b is left or dist.b is right:
                dist.b = parent

        s = sorted(set(s), reverse=True)

    #graph.write_png('cluster.png')
    return parent


if __name__ == '__main__':
    maketree()
