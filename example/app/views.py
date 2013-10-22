#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render
from app.tables import PersonTable


def base(request):
    people = PersonTable()
    return render(request, "index.html", {'people': people})


def linkcolumn(request):
    people = LinkColumnTable()
    return render(request, "index.html", {'people': people})
