#!/usr/bin/env python
# encoding: utf-8


class Cluster:
    def __init__(self, docs, left=None, right=None, name=''):
        self.docs = docs
        self.left = left
        self.right = right
        self.name = name

    def __repr__(self):
        return self.name
