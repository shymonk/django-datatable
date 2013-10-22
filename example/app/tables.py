#!/usr/bin/env python
# coding: utf-8

from table import Table, Column
from models import Person

class PersonTable(Table):
    id = Column(field='id', header=u'序号', header_attrs={'width': '50%'})
    name = Column(field='name', header=u'姓名', header_attrs={'width': '50%'})

    class Meta:
        model = Person
        id = 'people'
