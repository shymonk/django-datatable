#!/usr/bin/env python
# coding: utf-8

from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict
from columns import Column, BoundColumn
from addon import *
import copy
import traceback


class BaseTable(object):

    def __init__(self, data=None):
        if isinstance(data, QuerySet) or isinstance(data, list):
            self.data = data
        else:
            model = getattr(self.opts, 'model', None)
            if not model:
                raise ValueError("Model class or QuerySet-like object is required.")
            self.data = model.objects.all()

        # Make a copy so that modifying this will not touch the class definition.
        self.columns = copy.deepcopy(self.base_columns)
        # Build table add-ons
        self.addons = TableAddons(self)

    @property
    def rows(self):
        rows = []
        try:
            for obj in self.data:
                # Binding object to each column of each row, so that
                # data structure for each row is organized like this:
                # { boundcol0: td, boundcol1: td, boundcol2: td }
                row = SortedDict()
                columns = [BoundColumn(obj, col) for col in self.columns]
                for col in columns:
                    row[col] = col.html
                rows.append(row)
        except Exception, e:
            print e
            print traceback.format_exc()
        return rows

class TableAddons(object):
    def __init__(self, table):
        self.search_box = TableSearchBox(table.opts.search_placeholder,
                                         table.opts.disable_search)
        self.info_label = TableInfoLabel(table.opts.info_format,
                                         table.opts.disable_info)
        self.pagination = TablePagination(table.opts.pagination_first,
                                          table.opts.pagination_last,
                                          table.opts.pagination_prev,
                                          table.opts.pagination_next,
                                          table.opts.disable_pagination)
        self.length_menu = TableLengthMenu(table.opts.disable_length_menu)
        self.ext_button = TableExtButton(table.opts.ext_button_template,
                                         table.opts.ext_button_context)

    def render_dom(self):
        dom = "<'row'"
        dom += ''.join([self.ext_button.dom, self.search_box.dom])
        dom += "r>t<'row'"
        dom += ''.join([self.info_label.dom, self.pagination.dom, self.length_menu.dom])
        dom += ">"
        return mark_safe(dom)

class TableOptions(object):
    def __init__(self, clsname, options=None):
        self.model = getattr(options, 'model', None)

        # take class name in lowcase as default id of <table>
        self.id = getattr(options, 'id', clsname.lower())

        # build attributes for <table> tag, use bootstrap
        # css class "table table-boarded" as default style
        attrs = getattr(options, 'attrs', {})
        attrs['class'] = 'table table-bordered' + attrs.get('class', '')
        self.attrs = mark_safe(' '.join(['%s="%s"' % (attr_name, attr) for attr_name, attr in attrs.items()]))

        # inspect sorting option
        self.sort = []
        for column, order in getattr(options, 'sort', []):
            if not isinstance(column, int):
                raise ValueError('Sorting option must be organized by following'
                                 ' forms: [(0, "asc"), (1, "desc")]')
            if order not in ('asc', 'desc'):
                raise ValueError('Order value must be "asc" or "desc", '
                                 '"%s" is unsupported.' % order)
            self.sort.append((column, order))

        # options for table add-on
        self.disable_search = getattr(options, 'disable_search', False)
        self.search_placeholder = getattr(options, 'search_placeholder', 'Search')

        self.disable_info = getattr(options, 'disable_info', False)
        self.info_format = getattr(options, 'info_format', 'Total _TOTAL_')

        self.disable_pagination = getattr(options, 'disable_pagination', False)
        self.pagination_first = getattr(options, 'pagination_first', 'First')
        self.pagination_last = getattr(options, 'pagination_last', 'Last')
        self.pagination_prev = getattr(options, 'pagination_prev', 'Prev')
        self.pagination_next = getattr(options, 'pagination_next', 'Next')

        self.disable_length_menu = getattr(options, 'disable_length_menu', False)
        self.ext_button_template = getattr(options, 'ext_button_template', None)
        self.ext_button_context = getattr(options, 'ext_button_context', None)
        self.zero_records = getattr(options, 'zero_records', u'No records')

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
        attrs['base_columns'] = columns
        attrs['opts'] = TableOptions(name, meta)

        return super(TableMetaClass, cls).__new__(cls, name, bases, attrs)


Table = TableMetaClass('Table', (BaseTable,), {})

