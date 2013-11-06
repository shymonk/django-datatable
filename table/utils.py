#!/usr/bin/env python
# coding: utf-8

from django.db import models


class Accessor(str):
    """ A string describing a path from one object to another via attribute/index
        accesses. For convenience, the class has an alias `.A` to allow for more concise code.

        Relations are separated by a "." character.
    """
    SEPARATOR = '.'
    
    def resolve(self, context, quiet=False):
        """
        Return an object described by the accessor by traversing the attributes
        of context.

        """
        try:
            obj = context
            for level in self.levels:
                if isinstance(obj, dict):
                    obj = obj[level]
                elif isinstance(obj, models.Model):
                    if callable(level):
                        obj = getattr(obj, level)()
                    else:
                        # for model field that has choice set
                        # use get_xxx_display to access
                        display = 'get_%s_display' % level
                        obj = getattr(obj, display)() if hasattr(obj, display) else getattr(obj, level)
                if not obj:
                    break
            return obj
        except:
            if not quiet:
                raise

    @property
    def levels(self):
        if self == '':
            return ()
        return self.split(self.SEPARATOR)

A = Accessor
