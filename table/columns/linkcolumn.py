#!/usr/bin/env python
# coding: utf-8

from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
from table.utils import Accessor
from .base import Column

class LinkColumn(Column):
    def __init__(self, links, delimiter=u' ', *args, **kwargs):
        super(LinkColumn, self).__init__(*args, **kwargs)
        self.links = links
        self.delimiter = delimiter
        self.searchable = False
        self.safe = False

    def render(self, obj):
        return self.delimiter.join([link.render(obj) for link in self.links])

class Link(object):
    """ Represents a link element in html.
    """
    def __init__(self, text, viewname, args=None, kwargs=None, urlconf=None,
                 current_app=None, confirm=None):
        self.text = text
        self.viewname = viewname
        self.args = args or []
        self.kwargs = kwargs or {}
        self.urlconf = urlconf
        self.current_app = current_app
        self.confirm = confirm

    def resolve(self, obj):
        """ Resolving URL paths to the corresponding object. See:
            https://docs.djangoproject.com/en/dev/ref/urlresolvers/#reverse
        """
        viewname = self.viewname
        params = {}

        if self.args:
            params['args'] = [getattr(obj, attr) for attr in self.args]
        if self.kwargs:
            params['kwargs'] = {}
            for key, value in self.kwargs.itmes:
                params['kwargs'][key] = getattr(obj, value)
        if self.urlconf:
            params['urlconf'] = self.urlconf
        if self.current_app:
            params['current_app'] = self.current_app

        try:
            url = reverse(viewname, **params)
        except NoReverseMatch:
            url = ''
        return url
    
    def render(self, obj):
        """ Render link as HTML output tag <a>.
        """
        text = self.text.resolve(obj) if isinstance(self.text, Accessor) else self.text
        if self.confirm:
            return mark_safe(u'''<a href="%s" onclick="return confirm('%s')">%s</a>''' % 
                             (self.resolve(obj), self.confirm, text))
        else:
            return mark_safe(u'<a href="%s">%s</a>' % (self.resolve(obj), text))

