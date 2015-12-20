#!/usr/bin/env python
# coding: utf-8
from django.utils.html import escape

from table.utils import Accessor
from .base import Column


class DatetimeColumn(Column):

    DEFAULT_FORMAT = "%Y-%m-%d %H:%I:%S"

    def __init__(self, field, header=None, format=None, **kwargs):
        self.format = format or DatetimeColumn.DEFAULT_FORMAT
        super(DatetimeColumn, self).__init__(field, header, **kwargs)

    def render(self, obj):
        datetime = Accessor(self.field).resolve(obj)
        text = datetime.strftime(self.format)
        return escape(text)
