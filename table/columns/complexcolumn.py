#!/usr/bin/env python
# coding: utf-8

from .base import Column

class ComplexColumn(Column):
    def __init__(self, *args, **kwargs):
        super(ComplexColumn, *args, **kwargs)
    
    def extract(self):
        pass

