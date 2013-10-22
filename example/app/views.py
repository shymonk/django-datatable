#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render
from app.tables import PersonTable


def people(request):
    people = PersonTable()
    return render(request, "index.html", {'people': people})
