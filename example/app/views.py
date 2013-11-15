#!/usr/bin/env python
# coding: utf-8

from django.shortcuts import render
from tables import PersonTable


def base(request):
    people = PersonTable()
    return render(request, "index.html", {'people': people})

def edit(request, id):
    pass
