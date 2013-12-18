#!/usr/bin/env python
# coding: utf-8

import calendar
from .base import Column, ComplexColumn

class MonthsColumn(ComplexColumn):
    def __init__(self, start_date, end_date, month_name=None, *args, **kwargs):
        super(MonthsColumn, self).__init__(*args, **kwargs)
        self.start_date = start_date
        self.end_date = end_date
        self.month_name = month_name or calendar.month_name[1:]
        self.field = kwargs.pop('field')
        self.header_attrs = kwargs.pop('header_attrs', {})
        self.args = args
        self.kwargs = kwargs

    @property
    def cols_count(self):
        delta_year = self.end_date.year - self.start_date.year
        delta_month = self.end_date.month - self.start_date.month
        return delta_year * 12 + delta_month + 1

    @property
    def cols_names(self):
        names = []
        start_month = self.start_date.month
        for i in range(self.cols_count):
            names.append(self.month_name[(i + start_month - 1) % 12])
        return names

    @property
    def columns(self):
        return [self.get_col_obj(i) for i in range(self.cols_count)]

    def get_col_header(self, index):
        return self.cols_names[index]

    def get_col_header_attrs(self, index):
        attrs = {}
        self.header_attrs.update(attrs)
        return self.header_attrs

    def get_col_field(self, index):
        return '.'.join([self.field, str(index)])

    def get_col_obj(self, index):
        return Column(field=self.get_col_field(index),
                      header=self.get_col_header(index),
                      header_attrs=self.get_col_header_attrs(index),
                      **self.kwargs)

    def extract(self):
        return self.columns

class DaysColumn(ComplexColumn):
    def __init__(self, start_date, end_date, *args, **kwargs):
        super(MonthsColumn, self).__init__(*args, **kwargs)
        self.start_date = start_date
        self.end_date = end_date
        self.field = kwargs.pop('field')
        self.header_attrs = kwargs.pop('header_attrs', {})
        self.args = args
        self.kwargs = kwargs

    @property
    def cols_count(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def cols_names(self):
        names = []
        start_month = self.start_date.month
        for i in range(self.cols_count):
            names.append(self.month_name[(i + start_month - 1) % 12])
        return names

    @property
    def columns(self):
        return [self.get_col_obj(i) for i in range(self.cols_count)]

    def get_col_attr(self):
        pass

    def extract(self):
        pass

class WeeksColumn(ComplexColumn):
    pass

class CalendarColumn(ComplexColumn):
    def __init__(self, start_date, end_date, *args, **kwargs):
        super(ComplexColumn, self).__init(*args, **kwargs)
        self.month_column = None
        self.week_column = None
        self.days_column = None

    def get_month_col_attr(self):
        pass

    def get_week_col_attr(self):
        pass

    def get_day_col_attr(self):
        pass

    def extract(self):
        cols = []
        for col in [self.month_column, self.week_column, self.days_column]:
            cols.extend(col.extract())
        return cols
