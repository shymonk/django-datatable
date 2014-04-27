#!/usr/bin/env python
# coding: utf-8

from datetime import date
from table.columns import Column, LinkColumn, DatetimeColumn, Link
from table.columns.calendarcolumn import MonthsColumn, WeeksColumn, DaysColumn, CalendarColumn
from table.columns.sequencecolumn import SequenceColumn
from table.utils import A
from table import Table
from models import Person


class PersonTable(Table):
    id = Column(field='id', header=u'#')
    name = Column(field='name', header=u'NAME') 

    class Meta:
        model = Person


class SequenceColumnTable(Table):
    id = Column(field='id', header=u'#')
    seq = SequenceColumn(field='calendar', headers=["A", "B", "C", "D", "E"])


class CalendarColumnTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'rowspan': '3'})
    name = Column(field='name', header=u'NAME', header_attrs={'rowspan': '3'})
    calendar = CalendarColumn(field='calendar', start_date=date(2014, 4, 27), end_date=date(2014, 5, 9))


class AjaxDataTable(Table):
    id = Column(field='id', header=u'#')
    name = Column(field='name', header=u'NAME')

    class Meta:
        model = Person
        ajax = True

