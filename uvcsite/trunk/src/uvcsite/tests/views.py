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



class Index(megrok.layout.Page):
    grok.title('Startseite')
    grok.context(IUVCSite)
    navigation.sitemenuitem(BausAuskunft)

    daterows = [{
                'items' : [{
                        'date' : 'Yesterday!',
                        'content' : 'lolcontent'
                }]
        }]


    def update(self):
        self.flash('Warning', type="warning")
        self.flash('MESSAGE', type="error")
        self.flash('Nachricht')



class Kontakt(megrok.layout.Page):
    navigation.sitemenuitem(BausAuskunft)
    grok.name('Kontakt')
    grok.title('Kontakt')
    grok.context(Interface)

    def render(self):
        return "Kontakt"




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
