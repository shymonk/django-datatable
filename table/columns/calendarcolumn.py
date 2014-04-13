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
    WEEK_NAME = calendar.day_abbr

    def __init__(self, field, start_date, end_date, **kwargs):
        days = (end_date - start_date).days + 1
        dates = [start_date + timedelta(day) for day in range(days)]
        format_dates = [self.WEEK_NAME[date.weekday()] for date in dates]
        super(WeeksColumn, self).__init__(field, format_dates, **kwargs)


class MonthsColumn(SequenceColumn):
    MONTH_NAME = calendar.month_name[1:]

    def __init__(self, field, start_date, end_date, month_name=None, **kwargs):
        delta_year = end_date.year - start_date.year
        delta_month = end_date.month - start_date.month
        months = delta_year * 12 + delta_month + 1
        format_dates = [self.MONTH_NAME[(start_date.month + month - 1) % 12]
                        for month in range(months)]
        super(MonthsColumn, self).__init__(field, format_dates, **kwargs)


class InlineMonthsColumn(MonthsColumn):
    MONTH_NAME = [u'一月', u'二月', u'三月', u'四月', u'五月', u'六月',
                  u'七月', u'八月', u'九月', u'十月', u'十一月', u'十二月']

    def __init__(self, field, start_date, end_date, **kwargs):
        self.start_date = start_date
        self.end_date = end_date
        kwargs['space'] = False
        kwargs['sortable'] = False
        super(InlineMonthsColumn, self).__init__(field, start_date, end_date, **kwargs)

    def get_column(self, key):
        return Column(field=self.get_field(key),
                      header=self.get_header(key),
                      header_attrs=self.get_column_header_attrs(key),
                      **self.kwargs)

    def get_column_header_attrs(self, index):
        header_attrs = self.kwargs.pop("header_attrs", {})
        header_attrs.update({"colspan": self.get_column_span(index)})
        return header_attrs

    def get_column_span(self, index):
        """
        Get `colspan` value for <th> tag. It will render as
        <th colspan="VALUE"><th>
        """
        return str(self.get_days_span(index))

    def get_days_span(self, month_index):
        """
        Calculate the number of days the month spans.
        """
        base, end = self.start_date, self.end_date
        length = self.__len__()
        # If there's one month only, use difference of date
        # Otherwise, take date of last month or remaining days
        # of others as span value
        if length == 1:
            return end.day - base.day + 1
        is_first_month = month_index == 0
        is_last_month = month_index == length - 1
        if is_last_month:
            return end.day
        year = base.year + (base.month + month_index) / 13
        month = (base.month + month_index) % 12 or 12
        day = base.day if is_first_month else 1
        return get_month_remaining_days(year, month, day)


class InlineWeeksColumn(WeeksColumn):
    WEEK_NAME = ['M', 'T', 'W', 'T', 'F', 'S', 'S']

    def __init__(self, field, start_date, end_date, **kwargs):
        kwargs['space'] = False
        kwargs['sortable'] = False
        kwargs.setdefault('header_attrs', {})
        kwargs['header_attrs'].update({'class': 'calendar'})
        super(InlineWeeksColumn, self).__init__(field, start_date, end_date, **kwargs)

class InlineDaysColumn(DaysColumn):
    def __init__(self, field, start_date, end_date, **kwargs):
        kwargs['sortable'] = False
        kwargs.setdefault('header_attrs', {})
        kwargs['header_attrs'].update({'class': 'calendar'})
        super(InlineDaysColumn, self).__init__(field, start_date, end_date, **kwargs)

class CalendarColumn(SequenceColumn):
    MonthsColumnClass = InlineMonthsColumn
    WeeksColumnClass = InlineWeeksColumn
    DaysColumnClass = InlineDaysColumn

    def __init__(self, field, start_date, end_date, **kwargs):
        self.months_column = self.MonthsColumnClass(None, start_date, end_date, **kwargs)
        self.weeks_column = self.WeeksColumnClass(None, start_date, end_date, header_row_order=1)
        self.days_column = self.DaysColumnClass(field, start_date, end_date, header_row_order=2)
        headers = self.months_column.headers + self.weeks_column.headers + self.days_column.headers
        super(CalendarColumn, self).__init__(field, headers, **kwargs)

    @property
    def columns(self):
        columns = []
        columns.extend(self.months_column)
        columns.extend(self.weeks_column)
        columns.extend(self.days_column)
        return columns
