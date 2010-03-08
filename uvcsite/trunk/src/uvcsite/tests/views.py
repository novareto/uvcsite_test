# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout

from dolmen.menu import menuentry
from zope.interface import Interface
from uvcsite.interfaces import IUVCSite, IPersonalMenu, IDocumentActions, ISidebar, IFooter, IPersonalPreferences
from uvc.layout.menus import SidebarMenu
from megrok.z3ctable import TablePage, Column, table


@menuentry(SidebarMenu)
class Index(megrok.layout.Page):
    grok.context(IUVCSite)
    grok.require('zope.View')

    def update(self):
        self.flash('MESSAGE', type="error")
        self.flash('Nachricht')


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

    def image_url(self):
        return self.application_url() + '/pdf.png'



@menuentry(SidebarMenu)
class Table(TablePage):
    grok.context(IUVCSite)
    grok.require('zope.View')

    startBatchingAt = 5
    batchSize = 5


    @property
    def values(self):
        print "values"
        return range(100)


class Number(Column):
    table(Table)
    grok.context(IUVCSite)
    header = "Number"

    def renderCell(self, item):
        return item
