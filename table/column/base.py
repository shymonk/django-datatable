#!/usr/bin/env python
# coding: utf-8

class Column(object):
    def __init__(self, index=False, title=None, field=None, width=None):
        self.index = index
        self.title = title
        self.width = width
        self.field = field
