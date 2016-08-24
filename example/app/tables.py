#!/usr/bin/env python
# coding: utf-8

from datetime import date
import django

if django.VERSION >= (1, 10):
    from django.urls import reverse_lazy
else:
    from django.core.urlresolvers import reverse_lazy

from table.columns import Column
from table.columns.calendarcolumn import CalendarColumn
from table.columns.sequencecolumn import SequenceColumn
from table.columns.imagecolumn import ImageColumn
from table.columns.linkcolumn import LinkColumn, Link, ImageLink
from table.columns.checkboxcolumn import CheckboxColumn
from table import Table
from table.utils import A

from app.models import Person


class ModelTable(Table):
    id = Column(field='id', header=u'#')
    name = Column(field='name', header=u'NAME')

    class Meta:
        model = Person


class AjaxTable(Table):
    id = Column(field='id', header=u'#')
    name = Column(field='name', header=u'NAME')
    organization = Column(field='organization.name', header=u'ORG')

    class Meta:
        model = Person
        ajax = True


class AjaxSourceTable(Table):
    id = Column(field='id', header=u'#')
    name = Column(field='name', header=u'NAME')

    class Meta:
        model = Person
        ajax = True
        ajax_source = reverse_lazy('ajax_source_api')


class SequenceColumnTable(Table):
    id = Column(field='id', header=u'#')
    seq = SequenceColumn(field='calendar', headers=["A", "B", "C", "D", "E"])


class CalendarColumnTable(Table):
    id = Column(field='id', header=u'#', header_attrs={'rowspan': '3'})
    name = Column(field='name', header=u'NAME', header_attrs={'rowspan': '3'})
    calendar = CalendarColumn(field='calendar', start_date=date(2014, 4, 27), end_date=date(2014, 5, 9))


image_url = 'https://cdn0.iconfinder.com/data/icons/users-android-l-lollipop-icon-pack/24/user-32.png'


class LinkColumnTable(Table):
    id = Column(field='id', header=u'#')
    name = LinkColumn(header=u'NAME', links=[
        Link(viewname='user_profile', args=(A('id'),), text=A('name'))])
    avatar = LinkColumn(header=u'AVATAR', links=[
        ImageLink(viewname='user_profile', args=(A('id'),), image=image_url, image_title='avatar')])
    # logo = ImageColumn(field='logo.url', header=u'Logo Image', image_title='logo')

    class Meta:
        model = Person


class CheckboxColumnTable(Table):
    id = Column(field='id', header=u'#')
    name = Column(field='name', header=u'NAME')
    married = CheckboxColumn(field='married', header=u'MARRIED')

    class Meta:
        model = Person
