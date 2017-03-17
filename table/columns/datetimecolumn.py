#!/usr/bin/env python
# coding: utf-8
from django.utils.html import escape

from table.settings import TABLE_ATTR_DEFAULT_DATE_FORMAT
from table.utils import Accessor
from .base import Column


class DatetimeColumn(Column):

    DEFAULT_FORMAT = TABLE_ATTR_DEFAULT_DATE_FORMAT

    def __init__(self, field, header=None, format=None, **kwargs):
        self.format = format or DatetimeColumn.DEFAULT_FORMAT
        super(DatetimeColumn, self).__init__(field, header, **kwargs)

    def render(self, obj):
        datetime = Accessor(self.field).resolve(obj)
        text = datetime.strftime(self.format)
        return escape(text)
