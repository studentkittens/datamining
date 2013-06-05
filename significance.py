#!/usr/bin/env python
# encoding: utf-8
from collections import Counter
from itertools import combinations
from math import log, factorial


def read_sentences(filename):
    sentences = []
    with open(filename, 'r') as file_handle:
        for line in file_handle:
            sentence = set(filter(None, [normalize(w) for w in line.split()]))
            sentences.append(sentence)
    return sentences


def normalize(word):
    return ''.join(filter(str.isalnum, word.lower()))


def count_words(sentences):
    ctr = Counter()
    lookup_table = {}
    for sentence in sentences:
        for word in sentence:
            lookup_table.setdefault(word, set()).add(tuple(sentence))
        ctr.update(sentence)
    return ctr, lookup_table


def significance(a, b, k, n):
    lam = a * b / n
    if (k + 1) / lam > 2.5:
        if k > 10:
            return (k * (log(k) - log(lam) - 1)) / log(n)
        return (lam - k * log(lam) + log(factorial(k))) / log(n)
    return 0


if __name__ == '__main__':
    sentences = read_sentences('lst.csv')
    words, lookup_table = count_words(sentences)
    unigrams = {k: v for k, v in words.items() if v > 49}

    bigram_counter = {}
    for a, b in combinations(unigrams.keys(), 2):
        intersect_len = len(lookup_table[a] & lookup_table[b])
        if intersect_len > 0:
            bigram_counter[(a, b)] = intersect_len

    sigs = {}
    for ab, k in bigram_counter.items():
        sigs[ab] = significance(words[ab[0]], words[ab[1]], k, len(sentences))

    sorted_sigs = sorted(sigs.items(), key=lambda t: t[1], reverse=True)
    for ab, signum in sorted_sigs:
        print('ab: {} s: {} k: {} a: {} b: {}'.format(
            ab, signum, bigram_counter[ab], words[ab[0]], words[ab[1]]
        ))
