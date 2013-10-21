# Django-table
***

![preview](http://redmine.funshion.com/redmine/attachments/download/54280/django-table.png)

## Overview
---

Django-table is a simple Django app to origanize data in tabular form.
It is based on [datatable](http://datatables.net).

## Quick start
---
<br>
1. Setup Django-table application in Python environment:<br>

    $ python setup.py install
2. Add "table" to your INSTALLED_APPS setting like this:<br>

    INSTALLED_APPS = (
        ...,
        'table',
    )
3. Define a simple model named Person:<br>

    # example/app/models.py
    class Person(models.Model):
        name = models.CharField(max_length=100)
4. Add some data so you have something to display in the table.
Now define a PersonTable class without any options in table file.<br>

    # example/app/tables.py
    from models import Person
    from table import Table, Column
    
    class PersonTable(Table):
        id = Column(field='id')
        name = Column(field='name')

        class Meta:
            model = Person
            id = 'people'

And pass a table instance to the view.

    # example/app/views.py
    from django.shortcuts import render
    from app.tables import PersonTable

    def people(request):
        people = PersonTable()
        return render(request, "index.html", {'people': people})
5. Finally, implement the template:<br>

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

<br>
## Reference
---
### Table
#### DataSource
* Model
* Dict-List
* Json
#### Options
To define the model that bound to the table or customize attributes of the table, 
Provides a way to define global settings for table, as opposed to defining them for each instance.

* model
  
  > The model class that binded to the table, the queryset contains all objects for the model will be used to render table by default. It is the basic form to offer the data source.

  > **type**: classobj
  
  > **default**: None
  
  >     # models.py
  >     class Person(models.Model):
  >         name = models.CharField(max_length=40)
  > 
  >     # tables.py
  >     from table import Table, Column
  >
  >     class PersonTable(Table):
  >         id = Column(field='id')
  >         name = Column(field='name')
  >         class Meta:
  >             model = Person

* attrs
* sort
### Column
* Build-in Column
  * Column
  * Link Column
      > Renders value as an internal hyperlink to another page, such as UPDATE, DELETE. 

      > **class table.LinkColumn(links=[]):**

      > **Parameters**: 
      > * links: List of directory that key is content of < a > tag and value is the url that href specified, So:

      >         from table import LinkColumn
      >         c = LinkColumn(links=[{'update': 'http://update', 'delete': 'http://delete'}])
  * Checkbox Column

* Custom Column

  > If you want full control over the way the table is rendered, ignore the built-in Columns,
and instead pass an instance of your Table subclass into your own template. So you can define
a column with two hyperlink like this:
  
  
