# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout

from dolmen.menu import menuentry
from zope.interface import Interface
from uvcsite.interfaces import IUVCSite, IDocumentActions, ISidebar, IFooter, IPersonalPreferences


@menuentry(ISidebar)
class Index(megrok.layout.Page):
    grok.context(IUVCSite)
    grok.require('zope.View')


@menuentry(IFooter)
class Kontakt(megrok.layout.Page):
    grok.context(Interface)
    grok.require('zope.View')

    def render(self):
        return "Kontakt"


@menuentry(IDocumentActions)
class PdfIcon(grok.View):
    grok.name('aspdf')
    grok.context(IUVCSite)

    def render(self):
        return "PDF"

@menuentry(IPersonalPreferences)
class ENMS(megrok.layout.Page):
    grok.title('Mitbenutzerverwaltung')
    grok.name('Mitbenutzerverwaltung')
    grok.context(Interface)

    def render(self):
        return "ENMS"

