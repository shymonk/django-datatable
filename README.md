# Django-table


![preview](https://dl.dropboxusercontent.com/u/94696700/example.png)

***
## Overview
<br>
Django-table is a simple Django app to origanize data in tabular form.
It is based on [datatable](http://datatables.net) and [bootstrap](http://getbootstrap.com/).

## Requirement
<br>

* jQuery 1.6+

* Bootstrap 3.0

* Django 1.4+

## Quick start
<br>

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
## DataSource
<br>

* Model

  Use a django MTV model as table data source, and queries all data in database by default.
  see **model** in table options for details.

* QuerySet

  Similiar to **Model**, but pass queryset when you initialize table instance instead of defining model option.
  Basically, it used to filtering or sorting data your want to display in table.

        # models.py
        class Person(models.Model):
            name = models.CharField(max_length=100)
            
        # tables.py
        from models import Person
        from table import Table, Column

        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')
            
        # views.py
        from django.shortcuts import render
        from models import Person
        from app.tables import PersonTable

        def people(request):
            people = PersonTable(Person.objects.all())
            return render(request, "index.html", {'people': people})

## Columns
<br>

* Column

* Link Column

## Table Add-on
<br>

* search-box

* info-label

* pagination

* length-menu

* extense-button

## API Reference
<br>
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
  Placeholder attribute for search box.

  **type**: unicode

  **default**: u"Search"

* #### info
  This string gives information to the end user about the information that is current on display on the page.
  The `_START_`, `_END_`, `_TOTAL_` variables are all dynamically replaced as the table display updates, and can be freely moved or removed.

  **type**: unicode

  **default**: u"Total `_TOTAL_`"

* #### zero_records
  Text shown inside the table records when the is no information to be
  displayed after filtering. sEmptyTable is shown when there is simply no
  information in the table at all (regardless of filtering)

  **type**: unicode

  **default**: u"No records"

* #### page_first
  The text to use for pagination 'next' button.

  **type**: unicode

  **default**: u"First"

* #### page_last
  The text to use for pagination 'last' button.

  **type**: unicode

  **default**: u"Last"

* #### page_prev
  The text to use for pagination 'previous' button.

  **type**: unicode

  **default**: u"Prev"

* #### page_next
  The text to use for pagination 'previous' button.

  **type**: unicode

  **default**: u"Next"

* <h4 id="ext_button_link">ext_button_link</h4>
  The link for extense button(top-left corner). If provided, it will rendered as `<button href="ext_button_link">`,
  else, the extense button will be hided.

  **type**: string

  **default**: None

* <h4 id="ext_button_text">ext_button_text</h4>
  The text to use for extense button(top-left corner).

  **type**: unicode

  **default**: u"Add record"


### Build-in Column

* #### Column

    class *table.columns*.***Column***(*field=None*, *attrs=None*, *header=None*, *header_attrs=None*)

    A single column of table.

    **Parameters:**

    * **field**:
    
      For model data source, it is field name that corresponded to the current column. For dict-list data source, use the key instead.

      **type**: string

      **default**: None

    * **attrs**:
    
      Html attributes for `<td>` tag.

      Note: For object-related attribute, such as `<td title="xxx">`, use *Accessor* instance as attribute value. See example below.
    
      **type**: dict
    
      **default**: None

    * **header**:
    
      Title text of current column, will rendered as `<th>text</th>`
    
      **type**: string
    
      **default**: field value

    * **header_attrs**:
    
      Html attributes for `<th>` elements.
    
      **type**: dict
    
      **default**: None

    * **sortable**:
    
      If `False`, this column will not be allowed used for sorting.
    
      **type**: bool
    
      **default**: True

    * **searchable**:
    
      If `False`, this column will not be allowed used for searching.
    
      **type**: bool
    
      **default**: True

    * **safe**:
    
      If `True`, add [safe](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#safe)
      filter to column string. 
    
      **type**: bool
    
      **default**: True

    * **visible**:
    
      If `False`, this column will not be included in HTML output.
    
      **type**: bool
    
      **default**: True

    Example:

        # tables.py
        from table import Table
        from table.columns import Column
        from table.utils import A
        class PersonTable(Table):
            name = Column(field='name', header=u'姓名', attrs={'class': 'custom'}, header_attrs={'width': '50%'})
            addr = Column(field='addr', header=u'年龄', attrs={'title': A('addr')}, header_attrs={'width': '50%'})

* #### LinkColumn

    class *table.columns*.***LinkColumn***(*links*, *delimiter=' '*, **args*, ***kwrags*)

    Column with hyperlinks that link to another page, such as update, delete.

    **Parameters:**

    * **links**:

      List of *Link* instance. See *class table.columns.Link* for more details.

      **type**: *Link*

      **default**: *[]*

    * **delimiter**:

      Separate links in single column, use SPACE as default.

      **type**: string

      **default**: " "

    Example:

        # models.py
        from django.db import models
        class Person(models.Model):
            name = models.CharField(max_length=100)
        
        # urls.py
        urlpatterns = patterns('',
            url(r'^edit/(\d+)/$', 'app.views.edit', name='edit'),
        )
        
        # tables.py
        from table import Table
        from table.columns import LinkColumn, Link
        class PersonTable(Table):
            action = LinkColumn(header=u'操作', links=[Link(text=u'编辑', viewname='app.views.edit', args=('id',)),]

    class *table.columns*.***Link***(*text*, *viewname*, *args=[]*, *kwargs={}*, *urlconf=None*, *current_app=None*)

    Represents a label `<a>` with hyperlink, it will render as `<a  href="http://example.com">text</a>`

    **Parameters:**
    * **text**: content of tag `<a>`
    * **viewname**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
    * **args**: field names of model corresponded to the value that passed to the url pattern, see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
    * **kwargs**: key-value form for args
    * **urlconf**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
    * **current_app**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
    * **confirm**: If *True*, show confirmation dialog when link is clicked, Default is *False*.
    * **confirm_text**: Text of confirmation dialog, Default is *None*.


### Custom Column
If you want full control over the way the column is rendered, ignore the built-in Columns, and instead place an instance of Column subclass into your Table.
