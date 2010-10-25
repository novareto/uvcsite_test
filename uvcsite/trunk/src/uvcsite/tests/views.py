# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout

from dolmen.menu import menuentry, global_menuentry
from zope.interface import Interface
from uvcsite.interfaces import IMyHomeFolder, IUVCSite, IHelp, IPersonalMenu, IDocumentActions, ISidebar, IFooter, IPersonalPreferences
from uvc.layout.menus import DocumentActionsMenu
from megrok.z3ctable import TablePage, Column, table
from uvcsite.resources import UVCResources
from uvcsite import HelpPage
from megrok import navigation
import uvcsite
from uvc.layout.menus import SubMenu


class BausAuskunft(SubMenu):
    grok.name('BausAuskunft')
    grok.title('BausAuskunftsdienste')
    navigation.parentmenu(uvcsite.IGlobalMenu)
    grok.order(2500)

from zope import interface
class Klaus(grok.View):
    grok.context(interface.Interface)
    grok.require('zope.Public')

    def update(self):
        print "ROLES", self.request.principal.groups

    def render(self):
        return "BLA"


class Index(megrok.layout.Page):
    grok.title('Startseite')
    grok.context(IUVCSite)
    #navigation.sitemenuitem(BausAuskunft)
    grok.require('zope.View')

    def update(self):
        print self.request.principal.groups



class Table(TablePage):
    """
    """
    grok.context(IMyHomeFolder)
    grok.require('zope.View')
    cssClasses = {'table': 'tablesorter'}
    grok.title('Tabelle')
    title = "Tabelle"
    description = "Beispieltabelle"
    uvcsite.sectionmenu(uvcsite.IExtraViews)


    startBatchingAt = 10 
    batchSize = 10 

    @property
    def values(self):
        return range(100)


class Number(Column):
    table(Table)
    grok.context(IMyHomeFolder)
    header = "Number"
    cssClasses = {'td':'right',}

    def renderCell(self, item):
        return item

class SortNumber(Column):
    grok.name('hase')
    table(Table)
    grok.context(IMyHomeFolder)
    header = "SortNumber"

    def renderCell(self, item):
        return item
