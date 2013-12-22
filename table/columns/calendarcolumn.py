#!/usr/bin/env python
# coding: utf-8

import calendar
from datetime import timedelta
from .base import Column
from .sequencecolumn import SequenceColumn

class DaysColumn(SequenceColumn):
    def __init__(self, field, start_date, end_date, **kwargs):
        self.field = field
        self.start_date = start_date
        self.end_date = end_date
        self.header_attrs = kwargs.pop('header_attrs', {})
        self.kwargs = kwargs
        super(DaysColumn, self).__init__(field, **kwargs)

    @property
    def columns_count(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def columns_names(self):
        date_range = [self.start_date + timedelta(i) for i in range(self.columns_count)]
        return [date.strftime('%d') for date in date_range]

    @property
    def columns(self):
        return [self.get_column(i) for i in range(self.columns_count)]

    def get_column(self, index):
        return Column(field=self.get_column_field(index),
                      header=self.get_column_header(index),
                      header_attrs=self.get_column_header_attrs(index),
                      **self.kwargs)
 
    def get_column_field(self, index):
        if self.field:
            return '.'.join([self.field, str(index)])
        else:
            return self.field

    def get_column_header(self, index):
        return self.columns_names[index]

    def get_column_header_attrs(self, index):
        attrs = {}
        self.header_attrs.update(attrs)
        return self.header_attrs

    def extract(self):
        return self.columns

class WeeksColumn(DaysColumn):
    def __init__(self, field, start_date, end_date, week_name=None, **kwargs):
        super(WeeksColumn, self).__init__(field, start_date, end_date, **kwargs)
        self.week_name = week_name or calendar.day_abbr

    @property
    def columns_names(self):
        date_range = [self.start_date + timedelta(i) for i in range(self.columns_count)]
        return [self.week_name[date.weekday()] for date in date_range]

class MonthsColumn(DaysColumn):
    def __init__(self, field, start_date, end_date, month_name=None, **kwargs):
        super(MonthsColumn, self).__init__(field, start_date, end_date, **kwargs)
        self.month_name = month_name or calendar.month_name[1:]

    @property
    def columns_count(self):
        delta_year = self.end_date.year - self.start_date.year
        delta_month = self.end_date.month - self.start_date.month
        return delta_year * 12 + delta_month + 1

    @property
    def columns_names(self):
        names = []
        start_month = self.start_date.month
        for i in range(self.columns_count):
            names.append(self.month_name[(i + start_month - 1) % 12])
        return names
