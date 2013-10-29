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
- Setup Django-table application in Python environment:

        $ python setup.py install

- Add "table" to your INSTALLED_APPS setting like this:

        INSTALLED_APPS = (
            ...,
            'table',
        )

- Define a simple model named Person:

        # example/app/models.py
        class Person(models.Model):
            name = models.CharField(max_length=100)

- Add some data so you have something to display in the table.
Now define a PersonTable class without any options in table file.

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

- Finally, implement the template:

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
***
## Reference

### DataSource
* Model
* QuerySet

### Table Options
In order to define the model datasource, customize attributes of the table, table options provides a way to define global settings for table.

* #### model
  The model class that binded to the table, the queryset contains all objects for this model will be used to render table by default. It is the basic form to offer the data source.

  **type**: classobj
 
  **default**: None
  
        # models.py
        class Person(models.Model):
            name = models.CharField(max_length=40)
        
        # tables.py
        from table import Table, Column
        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')
            class Meta:
                model = Person


* #### id
  The id attribute for `<table>` tag, it will rendered as `<table id="id">`. If not present, it will use your table class name inherit from `table.Table` in lowcase form.

  **type**: string

  **default**: None

* #### attrs
  Allows custom HTML attributes to be specified which will be added to the `<table>` tag.
  Note: *attrs* should not contains *id* key.

  **type**: dict

  **default**: {}

        # tables.py
        from table import Table, Column
        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')
            class Meta:
                attrs = {'class': 'custom_class'}
* #### sort
  Allows changing default behavior about sorting. By this varible, you can define which column(s) the sort is performed upon, and the sorting direction.

  The *sort* list should contain an tuple for each column to be sorted initially containing the column's index and a direction string ('asc' or 'desc').
  
  **type**: list

  **default**: []

        # tables.py
        from table import Table, Column
        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')
            class Meta:
                sort = [(0, 'asc'), ('1', 'desc')]


* #### search_placeholder

* #### info

* #### zero_records

* #### page_first

* #### page_last

* #### page_prev

* #### page_next

* #### ext_button_text

* #### ext_button_link


### Column

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
