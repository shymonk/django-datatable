#!/usr/bin/env python
# coding: utf-8

from datetime import date
from table.columns import Column, LinkColumn, DatetimeColumn, Link
from table.columns.calendarcolumn import MonthsColumn, WeeksColumn
from table.utils import A
from table import Table
from models import Person


class PersonTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    name = Column(field='name', header=u'NAME') 
    action = LinkColumn(header=u'ACTION', links=[Link(text=u'edit', viewname='app.views.edit', args=(A('id'),))])

    class Meta:
        model = Person
        ext_button_template = "button.html"
        # disable_search = True
        # disable_info = True
        # disable_length_menu = True
        # disable_pagination = True

class ScheduleTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'width': '5%'})
    name = Column(field='name', header=u'NAME', header_attrs={'width': '15%'})
    month = MonthsColumn(date(2013, 12, 18), date(2014, 5, 1), field='calendar')
    # week = WeeksColumn(None, None)

