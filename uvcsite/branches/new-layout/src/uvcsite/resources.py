# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok

#from megrok import resource
#from hurry.jquery import jquery
#from hurry.jquerytools import jquerytools
#from zope.interface import Interface
#from uvc.layout.interfaces import IHeaders


#class UVCResources(resource.ResourceLibrary):
#    resource.name('uvcresource')
#    resource.path('static')
#
#    resource.resource('jquery.tablesorter.min.js', depends=[jquery,])
#    resource.resource('uvc_base.js', depends=[jquery,])
#    resource.resource('uvc_base.css')
#
#
#Overlay = resource.ResourceInclusion(
#    UVCResources, 'overlay.js', depends=[jquerytools])
#
#Tooltip = resource.ResourceInclusion(
#    UVCResources, 'tooltip.js', depends=[jquerytools])
#
#Mask = resource.ResourceInclusion(
#    UVCResources, 'jquery.maskedinput-1.3.js', depends=[jquerytools])
#
#
#class UVCResourceViewlet(grok.Viewlet):
#    grok.viewletmanager(IHeaders)
#    grok.context(Interface)
#
#    def render(self):
#        jquery.need()
#        jquerytools.need()
#        UVCResources.need()
#        return u''
