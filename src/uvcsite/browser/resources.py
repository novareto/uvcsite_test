# -*- coding: utf-8 -*-

import grok
from zope.interface import Interface


class Icons(grok.DirectoryResource):
    """Directory Resource for Icons like pdf.png
    """
    grok.name('uvc-icons')
    grok.path('icons')


class Favicon(grok.View):
    """ Helper for Favicon.ico Errors Request
    """
    grok.context(Interface)
    grok.name('favicon.ico')
    grok.require('zope.Public')

    def render(self):
        return "BLA"
