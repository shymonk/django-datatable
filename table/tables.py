#!/usr/bin/env python
# coding: utf-8


from column import Column
from django.db.models.query import QuerySet
from django.utils.datastructures import SortedDict


class BaseTable(object):

    def __init__(self, data=None):
        model = getattr(self.opts, 'model', None)
        if model:
            self.queryset = model.objects.all()
        else:
            if isinstance(data, QuerySet):
                self.queryset = data
            elif isinstance(data, list):
                self.list = data
            else:
                raise ValueError("Model class or QuerySet-like object is required.")

    @property
    def rows(self):
        rows = []
        objects = self.queryset if hasattr(self, 'queryset') else self.list
        for obj in objects:
            row = SortedDict()
            for col in self.columns:
                row[col] = col.render(obj)
            rows.append(row)
        return rows

class TableOptions(object):
    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)
        self.id = getattr(options, 'id', None)
        self.attrs = getattr(options, 'attrs', {})
        self.sort = getattr(options, 'sort', [])

class TableMetaClass(type):
    """ Meta class for create Table class instance.
    """

    def __new__(cls, name, bases, attrs):
        columns, meta = [], None
        # extract declared columns and meta
        for attr_name, attr in attrs.items():
            if isinstance(attr, Column):
                columns.append(attr)
            else:
                meta = attr

        columns.sort(key=lambda x: x.instance_order)
        attrs['columns'] = columns
        attrs['opts'] = TableOptions(meta)
        if not attrs['opts'].id:
            attrs['opts'].id = name.lower()

        return super(TableMetaClass, cls).__new__(cls, name, bases, attrs)


Table = TableMetaClass('Table', (BaseTable,), {})
