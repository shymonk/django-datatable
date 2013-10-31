#!/usr/bin/env python
# coding: utf-8


from table.utils import Accessor


class Column(object):
    
    instance_order = 0

    def __init__(self, field=None, sortable=True, searchable=True, safe=True,
                 visible=True, attrs=None, header=None, header_attrs=None):
        self.accessor = Accessor(field)
        self.attrs = attrs
        self.sortable = sortable
        self.searchable = searchable
        self.safe = safe
        self.visible = visible
        self.header = ColumnHeader(text=header, attrs=header_attrs)

        self.instance_order = Column.instance_order
        Column.instance_order += 1

    def as_html(self, obj):
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
        self.base_attrs = column.attrs
        
        # copy non-object-related attributes to self directly
        self.sortable = column.sortable
        self.searchable = column.searchable
        self.safe = column.safe
        self.visible = column.visible
        self.header = column.header

    @property
    def html(self):
        """ Content of <td> tag
        """
        return self.column.as_html(self.obj)

    @property
    def attrs(self):
        """ Attributes of <td> tag
        """
        attrs = []
        for attr_name, attr in self.base_attrs.items():
            if isinstance(attr, Accessor):
                attr = attr.resolve(self.obj)
            attrs.append("%s=%s" % (attr_name, attr))
        return " ".join(attrs)

class ColumnHeader(object):

    def __init__(self, text=None, attrs={}):
        self.text = text
        self.attrs = attrs
        
    def render_attrs(self):
        """ Render attributes of <th> to html.
        """
        html = ''
        for attr in self.attrs:
            html = html + '{0}={1}'.format(attr, self.attrs.get(attr))
        return html
