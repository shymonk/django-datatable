#!/usr/bin/env python
# coding: utf-8


class Accessor(str):
    """ A string describing a path from one object to another via attribute/index
        accesses. For convenience, the class has an alias `.A` to allow for more concise code.

        Relations are separated by a "." character.
    """
    SEPARATOR = '.'
    
    def resolve(self, context, safe=True, quiet=False):
        """
        Return an object described by the accessor by traversing the attributes
        of context.

        """
        pass

    @property
    def bits(self):
        if self == '':
            return ()
        return self.split(self.SEPARATOR)



A = Accessor
