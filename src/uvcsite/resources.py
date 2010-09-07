# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok

from megrok import resource
from hurry.jquery import jquery
from zope.interface import Interface
from uvc.layout.interfaces import IHeaders


class UVCResources(resource.ResourceLibrary):
    resource.name('uvcresource')
    resource.path('static')

    resource.resource('jquery.tablesorter.min.js')
    resource.resource('jquery.tools.min.js')
    resource.resource('uvc_base.js')
    resource.resource('uvc_base.css')
    resource.resource('uvc_hilfen.css')


Overlay = resource.ResourceInclusion(
    UVCResources, 'overlay.js', depends=[jquery])


class UVCResourceViewlet(grok.Viewlet):
    grok.viewletmanager(IHeaders)
    grok.context(Interface)

    def render(self):
        jquery.need()
        UVCResources.need()
        return u''

