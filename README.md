# Django-table
***

![preview](http://redmine.funshion.com/redmine/attachments/download/54280/django-table.png)

***
## Overview
<br>
Django-table is a simple Django app to origanize data in tabular form.
It is based on [datatable](http://datatables.net).

***
## Quick start
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

## Table
<br>

### DataSource

* Model
  
  

* Dict-List

* Json

  Developing

### Options

  To define the model that bound to the table or customize attributes of the table, 
Provides a way to define global settings for table, as opposed to defining them for each instance.

* model
  
  > The model class that binded to the table, the queryset contains all objects for the model will be used to render table by default. It is the basic form to offer the data source.

  > **type**: classobj
  
  > **default**: None
  >
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

## Column
<br>

### Build-in Column
  * **Column**
  
      > class table.columns.***Column***(*field=None*, *attrs=None*, *header=None*, *header_attrs=None*)

      > > A single column of table. 

      > > **Parameters:** 
      > > * **field**: 
        
      > >   For model data source, it is field name that corresponded to the current column. For dict-list data source, use the key instead.
      
      > >   **type**: string
      
      > >   **default**: None
      > > 
      > > * **attrs**: 
           
      > >   Html attributes for <td> elements.

      > >   **type**: dict
      
      > >   **default**: None
      
      > > * **header**:
      
      > >   Title text of current column, will rendered as <th>text</th>
      
      > >   **type**: string
      
      > >   **default**: field value
      
      > > * **header_attrs**:
      
      > >   Html attributes for <td> elements.
      
      > >   **type**: dict
      
      > >   **default**: None
      
      > > Example:
      > >
      >     # models.py
      >     from django.db import models
      >     class Person(models.Model):
      >         name = models.CharField(max_length=100)
      >         age = models.IntegerField()
      > > 
      >     # tables.py
      >     from table import Table
      >     from table.columns import Column
      >     class PersonTable(Table):
      >         name = Column(field='name', attrs={'class': 'custom'}, header=u'姓名', header_attrs={'width': '50%'})
      >         addr = Column(field='age', header=u'年龄', header_attrs={'width': '50%'})
    
  * **LinkColumn**

      > class table.columns.***LinkColumn***(*links*, *delimiter=' '*, **args*, ***kwrags*)

      > > Column with hyperlinks that link to another page, such as update, delete. 

      > > **Parameters:** 
      > > * **links**: List of *Link* instance. See *class table.columns.Link* for more details.
      > > * **delimiter**: Separate links in single column, use SPACE as default.
      > >
      > > Example:
      > >
      >     # models.py
      >     from django.db import models
      >     class Person(models.Model):
      >         name = models.CharField(max_length=100)
      > >        
      >     # urls.py
      >     urlpatterns = patterns('',
      >         url(r'^edit/(\d+)/$', 'app.views.edit', name='edit'),
      >     )
      > >
      >     # tables.py
      >     from table import Table
      >     from table.columns import LinkColumn, Link
      >     class PersonTable(Table):
      >         action = LinkColumn(header=u'操作', links=[Link(text=u'编辑', viewname='app.views.edit', args=('id',)),]
    
      > class table.columns.***Link***(*text*, *viewname*, *args=[]*, *kwargs={}*, *urlconf=None*, *current_app=None*)
      
      > > Represents a label `<a>` that defined hyperlink, it will render as `<a  href="http://example.com">text</a>` 
      
      > > **Parameters:**
      > > * **text**: content of tag `<a>`
      > > * **viewname**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
      > > * **args**: field names of model corresponded to the value that passed to the url pattern, see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
      > > * **kwargs**: key-value form for args
      > > * **urlconf**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
      > > * **current_app**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)


### Custom Column

  > If you want full control over the way the table is rendered, ignore the built-in Columns,
and instead pass an instance of your Table subclass into your own template.
