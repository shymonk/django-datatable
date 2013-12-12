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
        kwargs = {}
        if not self.opts.disable_search:
            kwargs['search_box'] = TableSearchBox(self.opts.search_placeholder)
        if not self.opts.disable_info:
            kwargs['info_label'] = TableInfoLabel(self.opts.info_format)
        if not self.opts.disable_pagination:
            kwargs['pagination'] = TablePagination(self.opts.pagination_first,
                                                   self.opts.pagination_last,
                                                   self.opts.pagination_prev,
                                                   self.opts.pagination_next)
        if not self.opts.disable_length_menu:
            kwargs['length_menu'] = TableLengthMenu()
        if self.opts.ext_button_link:
            kwargs['ext_button'] = TableExtButton(self.opts.ext_button_text,
                                                  self.opts.ext_button_link)
        self.addons = TableAddons(**kwargs)

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
    def __init__(self, search_box=None, info_label=None, pagination=None,
                 length_menu=None, ext_button=None):
        self.search_box = search_box
        self.info_label = info_label
        self.pagination = pagination
        self.length_menu = length_menu
        self.ext_button = ext_button

    def render_dom(self):
        dom = "<'row'"
        for addon in [self.ext_button, self.search_box]:
            if addon:
                dom += addon.dom
        dom += "r>t<'row'"
        for addon in [self.info_label, self.pagination, self.length_menu]:
            if addon:
                dom += addon.dom
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
        self.search_placeholder = getattr(options, 'search_placeholder', None)
        self.search_dom = getattr(options, 'search_dom', None)

        self.disable_info = getattr(options, 'disable_info', False)
        self.info_format = getattr(options, 'info_format', None)

        self.disable_pagination = getattr(options, 'disable_pagination', False)
        self.pagination_first = getattr(options, 'pagination_first', None)
        self.pagination_last = getattr(options, 'pagination_last', None)
        self.pagination_prev = getattr(options, 'pagination_prev', None)
        self.pagination_next = getattr(options, 'pagination_next', None)

        self.disable_length_menu = getattr(options, 'disable_length_menu', False)

        self.ext_button_text = getattr(options, 'ext_button_text', None)
        self.ext_button_link = getattr(options, 'ext_button_link', None)

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

