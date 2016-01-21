#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render

from table.views import FeedDataView

from app.tables import (
    ModelTable, AjaxTable, AjaxSourceTable,
    CalendarColumnTable, SequenceColumnTable,
    LinkColumnTable, CheckboxColumnTable
)


def base(request):
    table = ModelTable()
    return render(request, "index.html", {'people': table})


def ajax(request):
    table = AjaxTable()
    return render(request, "index.html", {'people': table})


def ajax_source(request):
    table = AjaxSourceTable()
    return render(request, "index.html", {'people': table})


class Foo(object):
    def __init__(self, id, name, calendar):
        self.id = id
        self.name = name
        self.calendar = calendar


def sequence_column(request):
    data = [
        Foo(1, 'A', [1, 2, 3, 4, 5]),
        Foo(2, 'B', [1, 2, 3, 4, 5]),
        Foo(3, 'C', [1, 2, 3, 4, 5])
    ]
    table = SequenceColumnTable(data)
    return render(request, "index.html", {'people': table})


def calendar_column(request):
    data = [
        Foo(1, 'A', range(1, 14)),
        Foo(2, 'B', range(1, 14)),
        Foo(3, 'C', range(1, 14))
    ]
    table = CalendarColumnTable(data)
    return render(request, "index.html", {'people': table})


def link_column(request):
    table = LinkColumnTable()
    return render(request, "index.html", {'people': table})


def checkbox_column(request):
    table = CheckboxColumnTable()
    return render(request, "index.html", {'people': table})


def user_profile(request, uid):
    from app.models import Person
    from django.http import HttpResponse
    from django.shortcuts import get_object_or_404
    person = get_object_or_404(Person, pk=uid)
    return HttpResponse("User %s" % person.name)


class MyDataView(FeedDataView):

    token = AjaxSourceTable.token

    def get_queryset(self):
        return super(MyDataView, self).get_queryset().filter(id__gt=5)
