# Django-table

![preview](https://dl.dropboxusercontent.com/u/94696700/example.png)

## Overview

Django-table is a simple Django app to origanize data in tabular form.
It is based on [datatable](http://datatables.net) and [bootstrap](http://getbootstrap.com/).

## Requirement

* jQuery 1.6+

* Bootstrap 3.0

* Django 1.4+

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
        from table import Table
        from table.columns import Column
        
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
        {% load table_tags %}

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

## Tag

Render the whole table by simple tag `{% render_table %}`, pass `Table` instance as single argument.

    {% render_table table %}


## DataSource

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
        from table import Table
	    from table.columns import Column

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

* Dict-List

  Use a list of directories as table data source. Fields which declared in columns correspond to the keys of directory.

		# tables.py
		from table import Table
	    from table.columns import Column

		class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')

		# views.py
        from django.shortcuts import render
        from app.tables import PersonTable

        def people(request):
			data = [{'id': 1, 'name': 'John'}, {'id': 2, 'name': 'Tom'}]
            people = PersonTable(data)
            return render(request, "index.html", {'people': people})
					


## Columns

* Column

* Link Column

* Datetime Column

## Table Add-on

* search-box

* info-label

* pagination

* length-menu

* extense-button

## API Reference

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
        from table import Table
        from table.columns import Column
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
        from table import Table
        from table.columns import Column
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
        from table import Table
        from table.columns import Column
        class PersonTable(Table):
            id = Column(field='id')
            name = Column(field='name')
            class Meta:
                sort = [(0, 'asc'), ('1', 'desc')]


* #### search
  Hide search box if False.

  **type**: boolean

  **default**: False

* #### search_placeholder
  Placeholder attribute for search box.

  **type**: unicode

  **default**: u"Search"

* #### info
  Hide info label if False.

  **type**: boolean

  **default**: False

* #### info_format
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

* #### pagination
  Disable paginate if False.

  **type**: boolean

  **default**: False

* #### pagination_first
  The text to use for pagination 'next' button.

  **type**: unicode

  **default**: u"First"

* #### pagination_last
  The text to use for pagination 'last' button.

  **type**: unicode

  **default**: u"Last"

* #### pagination_prev
  The text to use for pagination 'previous' button.

  **type**: unicode

  **default**: u"Prev"

* #### pagination_next
  The text to use for pagination 'previous' button.

  **type**: unicode

  **default**: u"Next"

* #### ext\_button
  Hide extense button if False.

  **type**: boolean

  **default**: False

* #### ext\_button\_template
  Template for rending extense button(top-left corner).

  **type**: string

  **default**: None

* #### ext\_button\_context
  Template context for rendering extense button.

  **type**: dict

  **default**: None


### Build-in Column

* #### Column

    ##### class *table.columns*.***Column***(*field=None*, *attrs=None*, *header=None*, *header_attrs=None*)

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

    ##### class *table.columns*.***LinkColumn***(*field=None*, *header=None*, *links=None*, *delimiter=' '*, **args*, ***kwrags*)

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

    ##### class *table.columns*.***Link***(*text*, *viewname*, *args=[]*, *kwargs={}*, *urlconf=None*, *current_app=None*)

    Represents a label `<a>` with hyperlink, it will render as `<a  href="http://example.com">text</a>`

    **Parameters:**
    * **text**: content of tag `<a>`, a unicode string or a *Accessor* instance.
    * **viewname**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
    * **args**: *Accessor* instance that represents field name of model corresponded to the value that passed to the url pattern, see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
    * **kwargs**: key-value form for args
    * **urlconf**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)
    * **current_app**: see [reverse](http://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse)

* #### DatetimeColumn

    ##### class *table.columns*.***DatetimeColumn***(*field=None*, *header=None*, *format=None*,  **args*, ***kwrags*)

    Accept [datetime](http://docs.python.org/2/library/datetime.html#datetime.datetime) object as column field and format to specific string.

    **Parameters:**

    * **format**:

      See [strftime](http://docs.python.org/2/library/datetime.html#datetime.date.strftime).      

      **type**: *string*

      **default**: *"%Y-%m-%d %H:%I:%S"*
	

### Custom Column
If you want full control over the way the column is rendered, ignore the built-in Columns, and instead place an instance of Column subclass into your Table.
