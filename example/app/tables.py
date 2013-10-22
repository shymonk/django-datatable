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
    id = Column(field='id', header=u'序号',)
    name = Column(field='name', header=u'姓名')
    action = LinkColumn(header=u'操作', links=[Link('update', args=['id',]),
                                               Link('delete', args=['id',])])

    class Meta:
        model = Person
    
