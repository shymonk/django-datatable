#!/usr/bin/env python
# coding: utf-8


from table.utils import Accessor
from django.utils.safestring import mark_safe


class Column(object):
    """ Represents a single column.
    """
    
    instance_order = 0

    def __init__(self, field=None, header=None, attrs=None, header_attrs=None,
                 header_row_order=0, sortable=True, searchable=True, safe=True,
                 visible=True, space=True):
        self.accessor = Accessor(field)
        self.attrs = attrs or {}
        self.sortable = sortable
        self.searchable = searchable
        self.safe = safe
        self.visible = visible
        self.space = space
        self.header = ColumnHeader(header, header_attrs, header_row_order)

        self.instance_order = Column.instance_order
        Column.instance_order += 1

    def __str__(self):
        return self.header.text

    def render(self, obj):
        return self.accessor.resolve(obj)

class BoundColumn(object):
    """ A run-time version of Column. The difference between 
        BoundColumn and Column is that BoundColumn objects include the
        relationship between a Column and a object. In practice, this
        means that a BoundColumn knows the "field value" given to the
        Column when it was declared on the Table.
    """
    def __init__(self, obj, column):
        self.obj = obj
        self.column = column
        self.base_attrs = column.attrs.copy()
        
        # copy non-object-related attributes to self directly
        self.sortable = column.sortable
        self.searchable = column.searchable
        self.safe = column.safe
        self.visible = column.visible
        self.header = column.header

    @property
    def html(self):
        return self.column.render(self.obj) or ''

    @property
    def attrs(self):
        attrs = {}
        context = self.obj
        for attr_name, attr in self.base_attrs.items():
            if isinstance(attr, Accessor):
                attrs[attr_name] = attr.resolve(context)
            else:
                attrs[attr_name] = attr
        return mark_safe(' '.join(['%s="%s"' % (attr_name, attr) for attr_name, attr in attrs.items()]))

class ColumnHeader(object):
    def __init__(self, text=None, attrs=None, row_order=0):
        self.text = text
        self.base_attrs = attrs or {}
        self.row_order = row_order

    @property
    def attrs(self):
        return mark_safe(' '.join(['%s="%s"' % (attr_name, attr) for attr_name, attr in self.base_attrs.items()]))
