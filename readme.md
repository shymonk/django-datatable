# Django-table

_____________________________________________________________________

## Overview
<br>
![preview](http://redmine.funshion.com/redmine/attachments/download/54280/django-table.png)
Django-table is a simple Django app to origanize data in tabular form.
It is based on [datatable](http://datatables.net).

## Quick start
<br>
**1**.Setup Django-table application in Python environment:<br>

    $ python setup.py install</pre>

**2**. Add "table" to your INSTALLED_APPS setting like this:<br>

    INSTALLED_APPS = (
        ...,
        'table',
    )

**3**. Define a simple model named Person:<br>

    # example/app/models.py
    class Person(models.Model):
        name = models.CharField(max_length=100)</pre>

**4**. Add some data so you have something to display in the table. Now write a view to pass people dictionary into a template, it contains three keys:<br>

- Name of table, it will render as the id attribute of table.<br>
- Head of table, it is a list of tuples, every tuple contains 2 elements: column name and corresponding attribute name of the model.<br>
- Body of table, it is a queryset.

x
    # example/app/views.py
    from django.shortcuts import render
    from app.models import Person

    def people(request):
        people = {}
        people['name'] = 'people'
        people['head'] = [(u'序号', 'id'), (u'姓名', 'name')]
        people['body'] = Person.objects.all()
        return render(request, "index.html", {'people': people})</pre>

**5**. Finally, implement the template:<br>

    {# example/templates/index.html}
    {% load static %}
    {% load table %}

    <link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet" media="screen">
    <script src="{% static 'js/jquery.min.js' %}"></script>
    <script src="{% static 'js/bootstrap.min.js' %}"></script>

    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="content-type" content="text/html; charset=utf-8" />
            <title>person</title>
        </head>
        <body>
            <div class="container" style="margin-top: 10px">
                <h1>people</h1>
                <br />
                {% render_table people %}
            </div>
        </body>
    </html>

