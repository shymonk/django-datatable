#!/usr/bin/env python
# coding: utf-8


from column import Column



class BaseTable(object):
    """ Main table base class.
    """
    
    def __init__(self, data=None):
        self.data = data


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
