django-datatable
================

|Build Status| |PyPI|

.. figure:: https://dl.dropboxusercontent.com/u/94696700/example.png
   :alt: preview

Overview
--------

django-datatable is a simple Django app to origanize data in tabular
form based on `datatable <http://datatables.net>`__ and
`bootstrap <http://getbootstrap.com/>`__.

It is worth mentioning that the design of this project makes reference
to `django-table2 <https://github.com/bradleyayers/django-tables2>`__
and is mainly for the purpose of learning. I really appreciate anyone
making a pull-request to improve it.

Requirements
------------

-  Python 2.x

-  jQuery 1.6+

-  Django 1.5+

-  Bootstrap 3.0

Quick start
-----------

-  Setup Django-datatable application in Python environment:

   ::

       $ pip install django-datatable

-  Define a simple model named Person:

   ::

       # example/app/models.py
       class Person(models.Model):
           name = models.CharField(max_length=100)

-  Add "table" to your INSTALLED\_APPS setting like this:

   ::

       INSTALLED_APPS = (
           ...,
           'table',
       )

-  Add some data so you have something to display in the table. Now
   define a PersonTable class without any options in the table file.

   ::

       # example/app/tables.py
       from models import Person
       from table import Table
       from table.columns import Column

       class PersonTable(Table):
           id = Column(field='id')
           name = Column(field='name')
           class Meta:
               model = Person

And pass a table instance to the view.

::

        # example/app/views.py
        from django.shortcuts import render
        from app.tables import PersonTable

        def people(request):
            people = PersonTable()
            return render(request, "index.html", {'people': people})

-  Finally, implement the template:

   ::

       {# example/templates/index.html}
       {% load static %}
       {% load table_tags %}

       <link href="{% static 'table/css/bootstrap.min.css' %}" rel="stylesheet">
       <script src="{% static 'table/js/jquery.min.js' %}"></script>
       <script src="{% static 'table/js/bootstrap.min.js' %}"></script>

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

Tag
---

Render the whole table by simple tag ``{% render_table %}``, pass
``Table`` instance as single argument.

::

    {% render_table table %}

DataSource
----------

-  Model

Uses a django MTV model as table data source, and queries all data in
database by default. See **model** in table options for details.

-  QuerySet

Similiar to **Model**, but pass queryset when you initialize the table
instance instead of defining model option. Basically, it is used to
filter or sort data you want to display in table.

::

    Models:

        # models.py
        class Person(models.Model):
            name = models.CharField(max_length=100)

    Tables:

        # tables.py
        from models import Person
        from table import Table
            from table.columns import Column

        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')

    Views:

        # views.py
        from django.shortcuts import render
        from models import Person
        from app.tables import PersonTable

        def people(request):
            people = PersonTable(Person.objects.all())
            return render(request, "index.html", {'people': people})

-  Dict-List

Use a list of dictionaries as table data source. Fields declared in
columns correspond to the dictionary keys.

::

    Tables:

        # tables.py
        from table import Table
        from table.columns import Column

        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')

    Views:

        # views.py
        from django.shortcuts import render
        from app.tables import PersonTable

        def people(request):
            data = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Tom'}]
            people = PersonTable(data)
            return render(request, "index.html", {'people': people})

-  Ajax

For large amounts of data, loading them on front-end entirely is
impossible. So, django-table provides a simle option 'ajax' to load data
from the server-side asynchronously.

Note that once toggling ``ajax``, the ``model`` option is necessary.
Django-table will do paging/searching/sorting based on
``ModelClass.objects.all()``.

::

    Urls:

        # urls.py
        urlpatterns = patterns('',
            url(r'^table/', include(table.urls')),
        )

    Tables:

        # tables.py
        from table import Table
        from table.columns import Column

        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')

            class Meta:
                model = Person
                ajax = True

If you want to customize base data, use ``ajax_source`` option and
implement your own Class-based View by subclassing ``FeedDataView``.

::

    Tables:

        # tables.py
        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')

            class Meta:
                model = Person
                ajax = True
                ajax_source = reverse_lazy('table_data')

    Urls:

        # urls.py
        urlpatterns = patterns('',
            url(r'^table/data/$', MyDataView.as_view(), name='table_data'),
        )

    Views:

        # views.py
        from table.views import FeedDataView
        from app.tables import PersonTable

        class MyDataView(FeedDataView):

            token = PersonTable.token

            def get_queryset(self):
                return super(MyDataView, self).get_queryset().filter(id__gt=5)

Columns
-------

-  Column

-  Link Column

-  Datetime Column

-  Checkbox Column

-  Sequence Column

-  Calendar Column

Widgets
-------

-  search-box

-  info-label

-  pagination

-  length-menu

-  extense-button

API Reference
-------------

-  `wiki <https://github.com/shymonk/django-datatable/wiki/API-Reference>`__

.. |Build Status| image:: https://travis-ci.org/shymonk/django-datatable.svg?branch=master
   :target: https://travis-ci.org/shymonk/django-datatable
.. |PyPI| image:: https://img.shields.io/pypi/v/django-datatable.png
   :target: https://pypi.python.org/pypi/django-datatable
