#!/usr/bin/env python
# coding: utf-8

import calendar
from datetime import timedelta
from table.columns.base import Column
from table.columns.sequencecolumn import SequenceColumn


class DaysColumn(SequenceColumn):
    def __init__(self, field, start_date, end_date, **kwargs):
        days = (end_date - start_date).days + 1
        dates = [start_date + timedelta(day) for day in range(days)]
        format_dates = [date.strftime("%d") for date in dates]
        super(DaysColumn, self).__init__(field, format_dates, **kwargs)


class WeeksColumn(SequenceColumn):
    def __init__(self, field, start_date, end_date, week_name=None, **kwargs):
        week_name = week_name or calendar.day_abbr

        days = (end_date - start_date).days + 1
        dates = [start_date + timedelta(day) for day in range(days)]
        format_dates = [week_name[date.weekday()] for date in dates]
        super(WeeksColumn, self).__init__(field, format_dates, **kwargs)


class MonthsColumn(SequenceColumn):
    def __init__(self, field, start_date, end_date, month_name=None, **kwargs):
        month_name = month_name or calendar.month_name[1:]

        delta_year = end_date.year - start_date.year
        delta_month = end_date.month - start_date.month
        months = delta_year * 12 + delta_month + 1
        format_dates = [month_name[(start_date.month + month - 1) % 12]
                        for month in range(months)]
        super(MonthsColumn, self).__init__(field, format_dates, **kwargs)
