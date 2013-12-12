#!/usr/bin/env python
# coding: utf-8

from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe
from django.utils.datastructures import SortedDict
from columns import Column, BoundColumn
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

    def render_ext_button(self):
        return ''

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
        self.search_placeholder = getattr(options, 'search_placeholder', u'搜索')
        self.info = getattr(options, 'info', u'总条目 _TOTAL_')
        self.zero_records = getattr(options, 'zero_records', u'无记录')

        self.page_first = getattr(options, 'page_first', '首页')
        self.page_last = getattr(options, 'page_last', '末页')
        self.page_prev = getattr(options, 'page_prev', '上一页')
        self.page_next = getattr(options, 'page_next', '下一页')

        self.ext_button_text = getattr(options, 'ext_button_text', u'添加记录 +')
        self.ext_button_link = getattr(options, 'ext_button_link', None)


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

