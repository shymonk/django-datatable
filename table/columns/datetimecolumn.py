#!/usr/bin/env python
# coding: utf-8

from .base import Column

class DatetimeColumn(Column):

    DEFAULT_FORMAT = "%Y-%m-%d %H:%I:%S"

    def __init__(self, field, header=None, format=None, **kwargs):
        self.format = format or DatetimeColumn.DEFAULT_FORMAT
        super(DatetimeColumn, self).__init__(field, header, **kwargs)

    def render(self, obj):
        datetime = super(DatetimeColumn, self).render(obj)
        return datetime.strftime(self.format)
            
