# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvc.layout.slots.managers

from zope.interface import Interface
from megrok.resourceviewlet import ResourceViewlet
from fanstatic import Resource, Library
from js.jquery import jquery
from js.jquery_tools import jquery_tools
from js.jquery_tablesorter import tablesorter


UVCResources = Library('uvcsresource', 'library')

Overlay = Resource(UVCResources, 'overlay.js', depends=[jquery_tools])

Tooltip = Resource(UVCResources, 'tooltip.js', depends=[jquery_tools])

Mask = Resource(UVCResources,
    'jquery.maskedinput-1.3.js', depends=[jquery_tools])


class UVCResourceViewlet(ResourceViewlet):
    grok.viewletmanager(uvc.layout.slots.managers.Resources)
    grok.context(Interface)

    resources = [jquery, jquery_tools, tablesorter]
