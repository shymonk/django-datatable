#!/usr/bin/env python
# coding: utf-8

from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.safestring import mark_safe
from .base import Column

class LinkColumn(Column):
    def __init__(self, links, delimiter=u' ', *args, **kwargs):
        super(LinkColumn, self).__init__(*args, **kwargs)
        self.links = links
        self.delimiter = delimiter
        self.searchable = False
        self.safe = False

    def render(self, obj):
        return self.delimiter.join([link.as_html(obj) for link in self.links])

class Link(object):
    """ Represents a link element in html.
    """
    def __init__(self, text, viewname, args=[], kwargs={}, urlconf=None, current_app=None):
        self.text = text
        self.viewname = viewname
        self.args = args
        self.kwargs = kwargs
        self.urlconf = urlconf
        self.current_app = current_app

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
    
    def as_html(self, obj):
        url = self.resolve(obj)
        html = '<a href="%s">%s</a>' % (url, self.text)
        return mark_safe(html)
