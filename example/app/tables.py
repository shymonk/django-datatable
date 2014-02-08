#!/usr/bin/env python
# coding: utf-8

from datetime import date
from table.columns import Column, LinkColumn, DatetimeColumn, Link
from table.columns.calendarcolumn import MonthsColumn, WeeksColumn, DaysColumn
from table.columns.sequencecolumn import SequenceColumn
from table.utils import A
from table import Table
from models import Person


class PersonTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    name = Column(field='name', header=u'NAME') 
    action = LinkColumn(header=u'ACTION', links=[Link(text=u'edit', viewname='app.views.edit', args=(A('id'),))])

    class Meta:
        model = Person


class SequenceColumnTable(Table):
    id = Column(field='id', header=u'#')
    seq = SequenceColumn(field='calendar', headers=["A", "B", "C", "D", "E"])


class ScheduleTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    name = Column(field='name', header=u'NAME', header_attrs={'width': '15%'})
    # days = DaysColumn(field='calendar', start_date=date(2013, 12, 18), end_date=date(2014, 1, 1))
    # weeks = WeeksColumn(field='calendar', start_date=date(2013, 12, 18), end_date=date(2014, 1, 1))
    # month = MonthsColumn(field='calendar', start_date=date(2013, 12, 18), end_date=date(2014, 5, 1))


class AjaxDataTable(Table):
    id = Column(field='id', header=u'#')
    name = Column(field='name', header=u'NAME') 

    class Meta:
        model = Person
        ajax = True

