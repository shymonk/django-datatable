#!/usr/bin/env python
# coding: utf-8
from table.columns.base import Column


class SequenceColumn(Column):
    def __init__(self, field, headers, **kwargs):
        self.headers = headers
        self.kwargs = kwargs
        super(SequenceColumn, self).__init__(field, **kwargs)

    @property
    def columns(self):
        return [self.get_column(key) for key in range(self.__len__())]

    def __str__(self):
        return str(self.columns)

    def __len__(self):
        return len(self.headers)

    def __getitem__(self, key):
        return self.columns[key]

    def __setitem__(self, key, value):
        self.columns[key] = value

    def get_column(self, key):
        return Column(field=self.get_field(key),
                      header=self.get_header(key),
                      **self.kwargs)

    def get_field(self, key):
        if self.field:
            return ".".join([self.field, str(key)])
        else:
            return None

    def get_header(self, key):
        return self.headers[key]
