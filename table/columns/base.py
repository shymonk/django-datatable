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

    def render_attrs(self, obj):
        """ Render attributes of <td> to html.
        """
        html = []
        for attr_name, attr in self.attrs.items:
            if isinstance(attr, Accessor):
                attr = attr.resolve(obj)
            html.append("%s=%s" % (attr_name, attr))
        return " ".join(html)

    def render(self, obj):
        """ Render content of <td> tag for current obj. 
        """
        return self.accessor.resolve(obj)

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

class BoundColumn(object):
    """ A run-time version of Column. The difference between 
        BoundColumn and Column is that BoundColumn objects include the
        relationship between a Column and a Table. In practice, this
        means that a BoundColumn knows the "field value" given to the
        Column when it was declared on the Table.
    """
    def __init__(self, table, column):
        self.table = table
        self.column = column

class BoundColumns(object):
    """ A BountColumn container. It is used to iterate in every columns
        for a table. 
    """
    def __init__(self, table):
        self.table = table

