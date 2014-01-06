#!/usr/bin/env python
# coding: utf-8

from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
from table.utils import Accessor
from .base import Column

class LinkColumn(Column):
    def __init__(self, field=None, header=None, links=None,
                 delimiter='&nbsp', **kwargs):
        self.links, self.delimiter = links, delimiter
        kwargs['safe'] = False
        super(LinkColumn, self).__init__(field, header, **kwargs)

    def render(self, obj):
        return self.delimiter.join([link.render(obj) for link in self.links])

class Link(object):
    """
    Represents a html <a> tag.
    """
    def __init__(self, text, viewname, args=None, kwargs=None, urlconf=None,
                 current_app=None):
        self.basetext = text
        self.viewname = viewname
        self.args = args or []
        self.kwargs = kwargs or {}
        self.urlconf = urlconf
        self.current_app = current_app

    @property
    def text(self):
        if isinstance(self.basetext, Accessor):
            return self.basetext.resolve(self.obj)
        return self.basetext

    @property
    def url(self):
        # The following params + if statements create optional arguments to
        # pass to Django's reverse() function.
        params = {}
        if self.args:
            params['args'] = [arg.resolve(self.obj)
                              if isinstance(arg, Accessor) else arg
                              for arg in self.args]
        if self.kwargs:
            params['kwargs'] = {}
            for key, value in self.kwargs.itmes:
                params['kwargs'][key] = (value.resolve(self.obj)
                                         if isinstance(value, Accessor) else value)        
        if self.urlconf:
            params['urlconf'] = (self.urlconf.resolve(self.obj)
                                 if isinstance(self.urlconf, Accessor)
                                 else self.urlconf)
        if self.current_app:
            params['current_app'] = (self.current_app.resolve(self.obj)
                                     if isinstance(self.current_app, Accessor)
                                     else self.current_app)

        return reverse(self.viewname, **params)
    
    def render(self, obj):
        """ Render link as HTML output tag <a>.
        """
        self.obj = obj
        if not self.url or not self.text:
            return ""
        return mark_safe(u'<a href="%s">%s</a>' % (self.url, self.text))

