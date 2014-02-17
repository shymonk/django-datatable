#!/usr/bin/env python
# coding: utf-8

import copy
import traceback
from uuid import uuid4
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict
from columns import Column, BoundColumn, SequenceColumn
from addon import (TableSearchBox, TableInfoLabel, TablePagination,
                   TableLengthMenu, TableExtButton)


class BaseTable(object):

    def __init__(self, data=None):
        self.data = TableData(data, self)
        
        # Make a copy so that modifying this will not touch the class definition.
        self.columns = copy.deepcopy(self.base_columns)
        # Build table add-ons
        self.addons = TableAddons(self)

    @property
    def rows(self):
        rows = []
        for obj in self.data:
            # Binding object to each column of each row, so that
            # data structure for each row is organized like this:
            # { boundcol0: td, boundcol1: td, boundcol2: td }
            row = SortedDict()
            columns = [BoundColumn(obj, col) for col in self.columns if col.space]
            for col in columns:
                row[col] = col.html
            rows.append(row)
        return rows

    @property
    def header_rows(self):
        """
        [ [header1], [header3, header4] ]
        """
        # TO BE FIX: refactor
        header_rows = []
        headers = [col.header for col in self.columns]
        for header in headers:
            if len(header_rows) <= header.row_order:
                header_rows.append([])
            header_rows[header.row_order].append(header)
        return header_rows


class TableData(object):
    def __init__(self, data, table):
        model = getattr(table.opts, "model", None)
        if (data is not None and not hasattr(data, "__iter__") or
            data is None and model is None):
            raise ValueError("Model option or QuerySet-like object data"
                             "is required.")
        if data is None:
            self.queryset = model.objects.all()
        elif isinstance(data, QuerySet):
            self.queryset = data
        else:
            self.list = list(data)

    @property
    def data(self):
        return self.queryset if hasattr(self, "queryset") else self.list

    def __len__(self):
        return (self.queryset.count() if hasattr(self, 'queryset')
                                      else len(self.list))

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]
    

class TableDataMap(object):
    """
    A data map that represents relationship between Table instance and
    Model.
    """
    map = {}

    @classmethod
    def register(cls, token, model, columns):
        TableDataMap.map[token] = (model, columns)

    @classmethod
    def get_model(cls, token):
        return TableDataMap.map.get(token)[0]

    @classmethod
    def get_columns(cls, token):
        return TableDataMap.map.get(token)[1]


class TableAddons(object):
    def __init__(self, table):
        options = table.opts
        self.length_menu = TableLengthMenu(visible=options.length_menu)
        self.info_label = TableInfoLabel(format=options.info_format,
                                         visible=options.info)
        self.search_box = TableSearchBox(placeholder=options.search_placeholder,
                                         visible=options.search)
        self.ext_button = TableExtButton(template=options.ext_button_template,
                                         context=options.ext_button_context,
                                         visible=options.ext_button)
        self.pagination = TablePagination(first=options.pagination_first,
                                          last=options.pagination_last,
                                          prev=options.pagination_prev,
                                          next=options.pagination_next,
                                          visible=options.pagination)

    def render_dom(self):
        dom = ''
        if self.search_box.visible or self.ext_button.visible:
            dom += "<'row'" + ''.join([self.ext_button.dom, self.search_box.dom]) + ">"
        dom += "rt"
        if self.info_label.visible or self.pagination.visible or self.length_menu.visible:
            dom += "<'row'" + ''.join([self.info_label.dom, self.pagination.dom, self.length_menu.dom]) + ">"
        return mark_safe(dom)


class TableOptions(object):
    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)

        # ajax option
        self.ajax = getattr(options, 'ajax', False)
        self.ajax_source = getattr(options, 'ajax_source', None)

        # id attribute of <table> tag
        self.id = getattr(options, 'id', None)

        # build attributes for <table> tag, use bootstrap
        # css class "table table-boarded" as default style
        attrs = getattr(options, 'attrs', {})
        attrs['class'] = 'table table-bordered ' + attrs.get('class', '')
        self.attrs = mark_safe(' '.join(['%s="%s"' % (attr_name, attr)
                                         for attr_name, attr in attrs.items()]))
        # build attributes for <thead> and <tbody>
        thead_attrs = getattr(options, 'thead_attrs', {})
        self.thead_attrs = mark_safe(' '.join(['%s="%s"' % (attr_name, attr)
                                         for attr_name, attr in thead_attrs.items()]))
        tbody_attrs = getattr(options, 'tbody_attrs', {})
        self.tbody_attrs = mark_safe(' '.join(['%s="%s"' % (attr_name, attr)
                                         for attr_name, attr in tbody_attrs.items()]))

        # scrolling option
        self.scrollable = getattr(options, 'scrollable', False)
        self.scrollinner = getattr(options, 'scrollinner', "150%")
        self.fixed_columns = getattr(options, 'fixed_columns', None)
        self.fixed_columns_width = getattr(options, 'fixed_columns_width', None)
        
        # inspect sorting option
        self.sort = []
        for column, order in getattr(options, 'sort', []):
            if not isinstance(column, int) or order not in ('asc', 'desc'):
                raise ValueError('Sorting option must be organized by following'
                                 ' forms: [(0, "asc"), (1, "desc")]')
            self.sort.append((column, order))

        # options for table add-on
        self.search = getattr(options, 'search', True)
        self.search_placeholder = getattr(options, 'search_placeholder', 'Search')

        self.info = getattr(options, 'info', True)
        self.info_format = getattr(options, 'info_format', 'Total _TOTAL_')

        self.pagination = getattr(options, 'pagination', True)
        self.pagination_first = getattr(options, 'pagination_first', 'First')
        self.pagination_last = getattr(options, 'pagination_last', 'Last')
        self.pagination_prev = getattr(options, 'pagination_prev', 'Prev')
        self.pagination_next = getattr(options, 'pagination_next', 'Next')

        self.length_menu = getattr(options, 'length_menu', True)

        self.ext_button = getattr(options, 'ext_button', False)
        self.ext_button_template = getattr(options, 'ext_button_template', None)
        self.ext_button_context = getattr(options, 'ext_button_context', None)

        self.zero_records = getattr(options, 'zero_records', u'No records')


class TableMetaClass(type):
    """ Meta class for create Table class instance.
    """

    def __new__(cls, name, bases, attrs):
        opts = TableOptions(attrs.get('Meta', None))
        # take class name in lower case as table's id
        if opts.id is None:
            opts.id = name.lower()
        attrs['opts'] = opts

        # extract declared columns
        columns = []
        for attr_name, attr in attrs.items():
            if isinstance(attr, SequenceColumn):
                columns.extend(attr)
            elif isinstance(attr, Column):
                columns.append(attr)
        columns.sort(key=lambda x: x.instance_order)

        # If this class is subclassing other tables, add their fields as
        # well. Note that we loop over the bases in reverse - this is
        # necessary to preserve the correct order of columns.
        parent_columns = []
        for base in bases[::-1]:
            if hasattr(base, "base_columns"):
                parent_columns = base.base_columns + parent_columns
        attrs['base_columns'] = parent_columns + columns

        if opts.ajax:
            attrs['token'] = uuid4().hex
            TableDataMap.register(attrs['token'], opts.model, attrs['base_columns'])

        return super(TableMetaClass, cls).__new__(cls, name, bases, attrs)


Table = TableMetaClass('Table', (BaseTable,), {})
