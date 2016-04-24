#!/usr/bin/env python
# coding: utf-8
import calendar
from datetime import timedelta

from table.columns.base import Column
from table.columns.sequencecolumn import SequenceColumn


class DaysColumn(SequenceColumn):
    def __init__(self, field=None, start_date=None, end_date=None, **kwargs):
        total_days = (end_date - start_date).days + 1
        headers = [(start_date + timedelta(day)).strftime("%d")
                   for day in range(total_days)]
        super(DaysColumn, self).__init__(field, headers, **kwargs)


class WeeksColumn(SequenceColumn):
    WEEK_NAME = calendar.day_abbr

    def __init__(self, field=None, start_date=None, end_date=None, **kwargs):
        total_days = (end_date - start_date).days + 1
        headers = [self.WEEK_NAME[(start_date + timedelta(day)).weekday()]
                   for day in range(total_days)]
        super(WeeksColumn, self).__init__(field, headers, **kwargs)


class MonthsColumn(SequenceColumn):
    MONTH_NAME = calendar.month_name[1:]

    def __init__(self, field=None, start_date=None, end_date=None, **kwargs):
        delta_year = end_date.year - start_date.year
        delta_month = end_date.month - start_date.month
        total_months = delta_year * 12 + delta_month + 1
        headers = [self.MONTH_NAME[(start_date.month + month - 1) % 12]
                   for month in range(total_months)]
        super(MonthsColumn, self).__init__(field, headers, **kwargs)


class InlineDaysColumn(DaysColumn):
    def __init__(self, field=None, start_date=None, end_date=None, **kwargs):
        kwargs['sortable'] = False
        kwargs.setdefault('header_attrs', {})
        kwargs['header_attrs'].update({'class': 'calendar'})
        super(InlineDaysColumn, self).__init__(field, start_date, end_date, **kwargs)


class InlineWeeksColumn(WeeksColumn):
    def __init__(self, start_date=None, end_date=None, **kwargs):
        kwargs['space'] = False
        kwargs['sortable'] = False
        kwargs.setdefault('header_attrs', {})
        kwargs['header_attrs'].update({'class': 'calendar'})
        super(InlineWeeksColumn, self).__init__(start_date=start_date, end_date=end_date, **kwargs)


class InlineMonthsColumn(MonthsColumn):
    def __init__(self, start_date=None, end_date=None, **kwargs):
        self.start_date = start_date
        self.end_date = end_date
        kwargs['space'] = False
        kwargs['sortable'] = False
        super(InlineMonthsColumn, self).__init__(start_date=start_date, end_date=end_date, **kwargs)

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
        Get `colspan` value for <th> tag.
        It will render as <th colspan="VALUE"><th>
        """
        return str(self.get_days_span(index))

    def get_days_span(self, month_index):
        """
        Calculate how many days the month spans.
        """
        is_first_month = month_index == 0
        is_last_month = month_index == self.__len__() - 1

        y = int(self.start_date.year + (self.start_date.month + month_index) / 13)
        m = int((self.start_date.month + month_index) % 12 or 12)
        total = calendar.monthrange(y, m)[1]

        if is_first_month and is_last_month:
            return (self.end_date - self.start_date).days + 1
        else:
            if is_first_month:
                return total - self.start_date.day + 1
            elif is_last_month:
                return self.end_date.day
            else:
                return total


class CalendarColumn(SequenceColumn):
    MonthsColumnClass = InlineMonthsColumn
    WeeksColumnClass = InlineWeeksColumn
    DaysColumnClass = InlineDaysColumn

    def __init__(self, field, start_date, end_date, **kwargs):
        self.months_column = self.MonthsColumnClass(start_date, end_date, **kwargs)
        self.weeks_column = self.WeeksColumnClass(start_date, end_date, header_row_order=1)
        self.days_column = self.DaysColumnClass(field, start_date, end_date, header_row_order=2)
        headers = self.months_column.headers + self.weeks_column.headers + self.days_column.headers
        super(CalendarColumn, self).__init__(field, headers, **kwargs)

    @property
    def columns(self):
        return self.months_column.columns + self.weeks_column.columns + self.days_column.columns
