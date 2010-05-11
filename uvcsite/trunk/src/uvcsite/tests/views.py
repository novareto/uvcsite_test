# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout

from dolmen.menu import menuentry
from zope.interface import Interface
from uvcsite.interfaces import IMyHomeFolder, IUVCSite, IHelp, IPersonalMenu, IDocumentActions, ISidebar, IFooter, IPersonalPreferences
from uvc.layout.menus import SidebarMenu
from megrok.z3ctable import TablePage, Column, table
from uvcsite.resources import UVCResources
from uvcsite import HelpPage

@menuentry(IHelp, context=Interface)
class GlobaleHilfe(HelpPage):
    grok.context(IUVCSite)
    grok.title('Hilfe zum Extranet')


@menuentry(SidebarMenu, context=Interface)
class Index(megrok.layout.Page):
    grok.title('Startseite')
    grok.context(IUVCSite)

    def update(self):
        self.flash('Warning', type="warning")
        self.flash('MESSAGE', type="error")
        self.flash('Nachricht')


@menuentry(IFooter)
class Kontakt(megrok.layout.Page):
    grok.name('Kontakt')
    grok.title('Kontakt')
    grok.context(Interface)

    def render(self):
        return "Kontakt"


@menuentry(IDocumentActions)
class PdfIcon(grok.View):
    grok.name('aspdf')
    grok.title('pdf')
    grok.context(IUVCSite)

    title ="aspdf"

    def render(self):
        return "FUCKU"



@menuentry(SidebarMenu)
class Table(TablePage):
    grok.context(IMyHomeFolder)
    grok.require('zope.View')
    cssClasses = {'table': 'tablesorter'}


    startBatchingAt = 5
    batchSize = 5

    @property
    def values(self):
        return range(100)


class Number(Column):
    table(Table)
    grok.context(IMyHomeFolder)
    header = "Number"

    def renderCell(self, item):
        return item

class SortNumber(Column):
    grok.name('hase')
    table(Table)
    grok.context(IMyHomeFolder)
    header = "SortNumber"

    def renderCell(self, item):
        return item
