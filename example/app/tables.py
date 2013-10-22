#!/usr/bin/env python
# coding: utf-8

from table.column import Column, LinkColumn
from table import Table
from models import Person


class PersonTable(Table):
    id = Column(field='id', header=u'序号', header_attrs={'width': '50%'})
    name = Column(field='name', header=u'姓名', header_attrs={'width': '50%'})

    class Meta:
        model = Person


class LinkColumnTable(Table):
    id = Column(field='id', header=u'序号', header_attrs={'width': '40%'})
    name = Column(field='name', header=u'姓名', header_attrs={'width': '40%'})
    action = LinkColumn(header=u'操作', header_attrs={'width': '20%'})

    class Meta:
        model = Person
    
