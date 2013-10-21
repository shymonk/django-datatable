#!/usr/bin/env python
# coding: utf-8

from table import Table, Column
from models import Person

class PersonTable(Table):
    class Meta:
        model = Person
        id = 'people'

    id = Column(field='id', title=u'序号', width='50%')
    name = Column(field='name', title=u'姓名', width='50%')

