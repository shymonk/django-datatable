#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import copy
from collections import OrderedDict
from hashlib import md5

from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe

from table.columns import Column, BoundColumn, SequenceColumn
from table.widgets import SearchBox, InfoLabel, Pagination, LengthMenu, ExtButton
from table.settings import *

class BaseTable(object):

    def __init__(self, data=None):
        self.data = TableData(data, self)

        # Make a copy so that modifying this will not touch the class definition.
        self.columns = copy.deepcopy(self.base_columns)
        # Build table add-ons
        self.addons = TableWidgets(self)

    @property
    def rows(self):
        rows = []
        for obj in self.data:
            # Binding object to each column of each row, so that
            # data structure for each row is organized like this:
            # { boundcol0: td, boundcol1: td, boundcol2: td }
            row = OrderedDict()
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
        if token not in TableDataMap.map:
            TableDataMap.map[token] = (model, columns)

    @classmethod
    def get_model(cls, token):
        return TableDataMap.map.get(token)[0]

    @classmethod
    def get_columns(cls, token):
        return TableDataMap.map.get(token)[1]


class TableWidgets(object):
    def __init__(self, table):
        opts = table.opts
        self.search_box = SearchBox(opts.search, opts.search_placeholder)
        self.length_menu = LengthMenu(opts.length_menu)
        self.info_label = InfoLabel(opts.info, opts.info_format)
        self.pagination = Pagination(opts.pagination,
                                     opts.page_length,
                                     opts.pagination_first,
                                     opts.pagination_last,
                                     opts.pagination_prev,
                                     opts.pagination_next)
        self.ext_button = ExtButton(opts.ext_button,
                                    opts.ext_button_template,
                                    opts.ext_button_template_name,
                                    opts.ext_button_context)

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
        attrs = getattr(options, 'attrs', TABLE_ATTR_ATTRS)
        attrs['class'] = 'table ' + attrs.get('class', '')
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
        self.scrollable = getattr(options, 'scrollable', TABLE_ATTR_SCROLLABLE)
        self.scrollinner = getattr(options, 'scrollinner', TABLE_ATTR_SCROLLINNER)
        self.fixed_columns = getattr(options, 'fixed_columns', TABLE_ATTR_FIXED_COLUMNS)
        self.fixed_columns_width = getattr(options, 'fixed_columns_width', TABLE_ATTR_FIXED_COLUMNS_WIDTH)

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
        self.search = getattr(options, 'search', TABLE_ATTR_SEARCH)
        self.search_placeholder = getattr(options, 'search_placeholder', TABLE_ATTR_SEARCH_PLACEHOLDER)

        self.info = getattr(options, 'info', TABLE_ATTR_INFO)
        self.info_format = getattr(options, 'info_format', TABLE_ATTR_INFO_FORMAT)

        self.pagination = getattr(options, 'pagination', TABLE_ATTR_PAGINATION)
        self.page_length = getattr(options, 'page_length', TABLE_ATTR_PAGE_LENGTH)
        self.pagination_first = getattr(options, 'pagination_first', TABLE_ATTR_PAGINATION_FIRST)
        self.pagination_last = getattr(options, 'pagination_last', TABLE_ATTR_PAGINATION_LAST)
        self.pagination_prev = getattr(options, 'pagination_prev', TABLE_ATTR_PAGINATION_PREV)
        self.pagination_next = getattr(options, 'pagination_next', TABLE_ATTR_PAGINATION_NEXT)

        self.length_menu = getattr(options, 'length_menu', TABLE_ATTR_LENGTH_MENU)

        self.ext_button = getattr(options, 'ext_button', TABLE_ATTR_EXT_BUTTON)
        self.ext_button_template = getattr(options, 'ext_button_template', TABLE_ATTR_EXT_BUTTON_TEMPLATE)
        self.ext_button_template_name = getattr(options, 'ext_button_template_name', TABLE_ATTR_EXT_BUTTON_TEMPLATE_NAME)
        self.ext_button_context = getattr(options, 'ext_button_context', TABLE_ATTR_EXT_BUTTON_CONTEXT)

        self.zero_records = getattr(options, 'zero_records', TABLE_ATTR_ZERO_RECORDS)
        self.theme_css_file = getattr(options, 'theme_css_file', TABLE_ATTR_THEME_CSS_FILE)
        self.theme_js_file = getattr(options, 'theme_js_file', TABLE_ATTR_THEME_JS_FILE)

        # option cutomize list of static to load
        self.media_js = getattr(options, 'media_js',TABLE_ATTR_MEDIA_JS)

        # option stateSave
        self.stateSave = getattr(options, 'stateSave', TABLE_ATTR_STATESAVE)
        self.stateDuration = getattr(options, 'stateDuration', TABLE_ATTR_STATEDURATION)

        # option language json
        self.language_static_json = getattr(options, 'language_static_json', TABLE_ATTR_LANGUAGE_STATIC_JSON)

        # option responsive
        self.responsive = getattr(options, 'responsive', TABLE_ATTR_RESPONSIVE)

        # option tooltip
        self.tooltip_name = getattr(options, 'tooltip_name', '')

        #Add custom function to InitComplete function
        self.init_complete = getattr(options, 'init_complete', None)


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
        base_columns = parent_columns + columns

        # For ajax data source, store columns into global hash map with
        # unique token key. So that, columns can be get to construct data
        # on views layer.
        token = md5(name.encode('utf-8')).hexdigest()

        if opts.ajax:
            TableDataMap.register(token, opts.model, copy.deepcopy(base_columns))

        attrs['token'] = token
        attrs['base_columns'] = base_columns

        return super(TableMetaClass, cls).__new__(cls, name, bases, attrs)


Table = TableMetaClass(str('Table'), (BaseTable,), {})
