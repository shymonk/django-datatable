#!/usr/bin/env python
# coding: utf-8


from django.shortcuts import render
from app.models import Person

def people(request):
    people = {}
    people['name'] = 'people'
    people['head'] = [(u'序号', 'id'), (u'姓名', 'name')]
    people['body'] = Person.objects.all()
    return render(request, "index.html", {'people': people})

