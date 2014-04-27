#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render
from tables import (PersonTable, CalendarColumnTable, SequenceColumnTable,
                    AjaxDataTable)


class Foo(object):
    def __init__(self, id, name, calendar):
        self.id = id
        self.name = name
        self.calendar = calendar


def base(request):
    people = PersonTable()
    return render(request, "index.html", {'people': people})


def sequence_column(request):
    data = [Foo(1, 'A', [1,2,3,4,5]), Foo(2, 'B', [1,2,3,4,5]), Foo(3, 'C', [1,2,3,4,5])]
    table = SequenceColumnTable(data)
    return render(request, "index.html", {'people': table})


def calendar_column(request):
    data = [Foo(1, 'A', range(1, 14)), Foo(2, 'B', range(1, 14)), Foo(3, 'C', range(1, 14))]
    table = CalendarColumnTable(data)
    return render(request, "index.html", {'people': table})


def ajax_data(request):
    table = AjaxDataTable()
    return render(request, "index.html", {'people': table})
