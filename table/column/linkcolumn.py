#!/usr/bin/env python
# coding: utf-8

from .base import Column

class LinkColumn(Column):
    def __init__(self, *args, **kwargs):
        super(LinkColumn, self).__init__(*args, **kwargs)

