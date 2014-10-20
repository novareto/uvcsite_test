# -*- coding: utf-8 -*-

import uvclight
from zope.interface import Interface


class Favicon(uvclight.View):
    """ Helper for Favicon.ico Errors Request
    """
    uvclight.context(Interface)
    uvclight.name('favicon.ico')
    uvclight.auth.require('zope.Public')

    def render(self):
        return "BLA"
