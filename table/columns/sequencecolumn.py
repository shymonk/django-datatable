#!/usr/bin/env python
# coding: utf-8

from .base import Column

class SequenceColumn(Column):
    def __init__(self, *args, **kwargs):
        super(SequenceColumn, self).__init__(*args, **kwargs)

    def extract(self):
        pass
