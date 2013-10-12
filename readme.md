=====
Django-table
=====

Table is a simple Django app to origanize data in tabular form.
It is based on [datatable](http://datatables.net).

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'table',
      )

2. Include the polls URLconf in your project urls.py like this::

      url(r'^table/', include('table.urls')),


