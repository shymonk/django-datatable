#!/usr/bin/env python
# coding: utf-8


from column import Column
from django.db.models.query import QuerySet


class BaseTable(object):

    def __init__(self, data=None):
        if data:
            if isinstance(data, QuerySet):
                self.queryset = data
            else isinstance(data, list):
                self.list = data
        else:
            model = getattr(self.opts, 'model')
            self.queryset = model.objects.all()

    @property
    def rows(self):
        return self.queryset if hasattr(self, 'queryset') else self.list

    def render(self):
        pass

class TableData(object):
    def __init__(self, data, table):
        """ Build table data to QuerySet.
        """
        if data:
            if isinstance(data, QuerySet):
                self.queryset = data
            else:
                # data is dict-list, construct it to QuerySet-like object
                pass
        else:
            model = getattr(self.opts, 'model')
            self.queryset = model.objects.all()



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
        attrs['columns'] = [value for key, value in attrs.items() if isinstance(value, Column)]
        attrs['opts'] = TableOptions(attrs.get('Meta', None))
        if not attrs['opts'].id:
            attrs['opts'].id = name.lower()
        return super(TableMetaClass, cls).__new__(cls, name, bases, attrs)


Table = TableMetaClass('Table', (BaseTable,), {})
