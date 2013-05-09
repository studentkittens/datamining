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

        self._norm_freq = [0.0 for voc in self._vocs]
        self._abs_freq = [0.0 for voc in self._vocs]
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

    @property
    def norm_freq(self):
        return self._norm_freq

    @property
    def abs_freq(self):
        return self._abs_freq

    def set_norm_freq(self, abs_freq, norm_freq, all_vocs):
        for idx, voc in enumerate(self._vocs):
            try:
                freq_idx = all_vocs.index(voc)
                self._norm_freq[idx] = norm_freq[freq_idx]
                self._abs_freq[idx] = abs_freq[freq_idx]
            except ValueError:
                pass
