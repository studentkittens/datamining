#!/usr/bin/env python
# encoding: utf-8
from collections import Counter
from itertools import combinations
from math import log, factorial
from pprint import pprint

def readSentences(filename):
    sents = []
    with open(filename,'r') as f:
        for r in f:
            sent = set()
            sents.append(sent)
            for w in r.split():
                w = normalize(w)
                if w: sent.add(w)
    return sents

def normalize(word):
    return ''.join(filter(str.isalnum, word.lower()))

def countWords(sents):
    c = Counter()
    adj = {}
    for sent in sents:
        for w in sent:
            c[w] += 1
            l = adj.get(w)
            if l is None:
                l = set()
                adj[w] = l
            l.add(tuple(sent))
    return c, adj

def sig(t, k, n, words):
    a = words[t[0]]
    b = words[t[1]]
    lam = a * b / n
    if (k+1) / lam > 2.5:
        if k > 10:
            return k * (log(k) - log(lam) -1) / log(n)
        else:
            return (lam - k * log(lam) + log(factorial(k))) / log(n)
    else:
        return 0




def main():
    sents = readSentences('lst.csv')
    #print(sents)
    words, adj  = countWords(sents)
    #print(adj)
    #print(words)
    unigrams = {k: v for k, v in words.items() if v > 49}
    #print(unigrams)
    print('n unigrams', len(unigrams))
    bigram_counter = Counter()
    for a, b in combinations(unigrams.keys(),2):
        la = adj[a]
        lb = adj[b]

        k = len(la.intersection(lb))
        if k > 0:
            bigram_counter[(a, b)] = k
    n = len(sents)

    sigs = {t : sig(t, k, n, words) for t,k in bigram_counter.items()}
    sorted_sigs = sorted(sigs.items(), key=lambda t: t[1], reverse=True)

    for ab, significance in sorted_sigs:
        print(ab, 's:', significance, 'k:', bigram_counter[ab], 'a', words[ab[0]], 'b', words[ab[1]])
    #pprint(sigs)

    print(n)

if __name__ == '__main__':
    main()
