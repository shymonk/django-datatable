#!/usr/bin/env python
# coding: utf-8
import time

from django.utils.html import escape
from django.utils.safestring import mark_safe


class Accessor(str):
    """ A string describing a path from one object to another via attribute/index
        accesses. For convenience, the class has an alias `.A` to allow for more concise code.

        Relations are separated by a "." character.
    """
    SEPARATOR = '.'

    def resolve(self, context, quiet=True):
        """
        Return an object described by the accessor by traversing the attributes
        of context.

        """
        try:
            obj = context
            for level in self.levels:
                if isinstance(obj, dict):
                    obj = obj[level]
                elif isinstance(obj, list) or isinstance(obj, tuple):
                    obj = obj[int(level)]
                else:
                    if callable(getattr(obj, level)):
                        try:
                            obj = getattr(obj, level)()
                        except KeyError:
                            obj = getattr(obj, level)
                    else:
                        # for model field that has choice set
                        # use get_xxx_display to access
                        display = 'get_%s_display' % level
                        obj = getattr(obj, display)() if hasattr(obj, display) else getattr(obj, level)
                if not obj:
                    break
            return obj
        except Exception as e:
            if quiet:
                return ''
            else:
                raise e

    @property
    def levels(self):
        if self == '':
            return ()
        return self.split(self.SEPARATOR)

A = Accessor


class AttributesDict(dict):
    """
    A `dict` wrapper to render as HTML element attributes.
    """
    def render(self):
        return mark_safe(' '.join([
            '%s="%s"' % (attr_name, escape(attr))
            for attr_name, attr in self.items()
        ]))


def timeit(func):
    def wrap(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        print('func: %r took: %f ms'.format(func.__name__, (te - ts) * 1000))
        return result
    return wrap
