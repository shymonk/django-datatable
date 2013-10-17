# Django-table

_____________________________________________________________________

## Overview
<br>
Django-table is a simple Django app to origanize data in tabular form.
It is based on [datatable](http://datatables.net).

## Quick start
<br>
1.Setup Django-table application in Python environment:

<pre>$ python setup.py install</pre>

2.Add "table" to your INSTALLED_APPS setting like this:

<pre>INSTALLED_APPS = (
    ...,
    'table',
)</pre>

3.Define a simple model named Person:

<pre>#example/app/models.py
class Person(models.Model):
    name = models.CharField(max_length=100)</pre>

4.Add some data so you have something to display in the table.Now write a view to pass people dictionary into a template,it contains three keys:<br>
* Name of table, it will render as the id attribute of table.<br>
* Head of table, it is a list of tuples, every tuple contains 2 elements: column name and corresponding attribute name of the model<br>
* Body of table, it is a queryset of mode.<br>
<pre># example/app/views.py
from django.shortcuts import render
from app.models import Person

def people(request):
    people = {}
    people['name'] = 'people'
    people['head'] = [(u'序号', 'id'), (u'姓名', 'name')]
    people['body'] = Person.objects.all()
    return render(request, "index.html", {'people': people})</pre>

5.Finally, implement the template:
<pre>{# example/templates/index.html}
{% load static %}
{% load table %}

< include jquery and bootstrap css and js files >

{% include 'table_include.html' %}
{% render_table people %}</pre>
