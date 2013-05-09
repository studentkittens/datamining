#!/usr/bin/env python
# encoding: utf-8


class Document:
    DOC_INDEX = 1

    def __init__(self, path, text, vocs):
        self._path = path
        self._text = text
        self._vocs = vocs
        self._name = 'd' + str(Document.DOC_INDEX)
        self._distances = {}
        Document.DOC_INDEX += 1

    @property
    def distances(self):
        return self._distances

    @property
    def path(self):
        return self._path

    @property
    def text(self):
        return self._text

    @property
    def vocs(self):
        return self._vocs

    @property
    def name(self):
        return self._name
