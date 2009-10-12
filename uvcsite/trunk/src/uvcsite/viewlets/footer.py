# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de


import grok
from uvcsite import uvcsiteMF as _
from zope.interface import Interface
from uvcsite.interfaces import IFooter
from uvcsite.viewlets.utils import MenuItem


class Impressum(MenuItem):
    grok.name(u'Impressum')
    grok.context(Interface)
    grok.viewletmanager(IFooter)
    grok.order(1)

    title = _(u'Impressum')
    urlEndings = "impressum"
    viewURL = "impressum"


class Barrierefreiheit(MenuItem):
    grok.name(u'Barrierefreiheit')
    grok.context(Interface)
    grok.viewletmanager(IFooter)
    grok.order(2)

    title = _(u'Barrierefreiheit')
    urlEndings = "barrierefreiheit"
    viewURL = "barrierefreiheit"


class Kontakt(MenuItem):
    grok.name(u'Kontakt')
    grok.context(Interface)
    grok.viewletmanager(IFooter)
    grok.order(3)

    title = _(u'Kontakt')
    css = "last"
    urlEndings = "kontakt"
    viewURL = "kontakt"
