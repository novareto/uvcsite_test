# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout

from dolmen.menu import menuentry
from zope.interface import Interface
from uvcsite.interfaces import IUVCSite, IPersonalMenu, IDocumentActions, ISidebar, IFooter, IPersonalPreferences
from uvc.layout.menus import SidebarMenu


@menuentry(SidebarMenu)
class Index(megrok.layout.Page):
    grok.context(IUVCSite)
    grok.require('zope.View')


@menuentry(IFooter)
class Kontakt(megrok.layout.Page):
    grok.name('Kontakt')
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

@menuentry(IPersonalMenu)
class Logout(grok.View):
    grok.title('Logout')
    grok.name('Logout')
    grok.context(Interface)

    def render(self):
        return "Logout"
