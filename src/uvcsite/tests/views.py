# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout

from dolmen.menu import menuentry, global_menuentry
from zope.interface import Interface
from uvcsite.interfaces import IMyHomeFolder, IUVCSite, IHelp, IPersonalMenu, IDocumentActions, ISidebar, IFooter, IPersonalPreferences
from uvc.layout.slots.menus import DocumentActionsMenu
from megrok.z3ctable import TablePage, Column, table
from uvcsite import HelpPage
import uvcsite
from zope.authentication.interfaces import IUnauthenticatedPrincipal


class Auskunftsdienste(uvcsite.SubMenu):
    grok.context(Interface)
    grok.name('BausAuskunft')
    grok.title('BausAuskunftsdienste')
    grok.viewletmanager(uvcsite.IGlobalMenu)
    grok.order(2500)


class LogoutMenu(uvcsite.MenuItem):
    grok.name('Logout')
    grok.title('Logout')
    grok.require('zope.View')
    grok.viewletmanager(uvcsite.IPersonalPreferences)

    action = "logout"


class Logout(grok.View):
    """ Logout View
    """
    grok.name('Logout')
    grok.title('Logout')
    grok.require('zope.View')
    grok.context(uvcsite.IUVCSite)
    grok.viewletmanager(uvcsite.IPersonalPreferences)

    KEYS = ("beaker.session", "dolmen.authcookie")

    def update(self):
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal):
            for key in self.KEYS:
                self.request.response.expireCookie(key, path='/')

    def render(self):
        return self.redirect(self.application_url()) 


class SSMenu(uvcsite.MenuItem):
    grok.context(Interface)
    grok.title('Startseite')
    grok.viewletmanager(Auskunftsdienste)

    action = "index"


class Index(uvcsite.Page):
    grok.title('Startseite')
    grok.context(IUVCSite)
    grok.require('zope.View')

    def update(self):
        self.flash('Fehlermeldung...', 'error')
        self.flash('Warnung...', 'warning')

from grokcore.chameleon.components import ChameleonPageTemplateFile
class SelectiveIndex(uvcsite.Page):
    grok.title('Selective Index')
    grok.context(IUVCSite)
    grok.require('zope.View')
 
    template = ChameleonPageTemplateFile('views_templates/index.cpt')

    def update(self):
        if self.request.principal.id == "0202020002":
            self.template = ChameleonPageTemplateFile('views_templates/index2.cpt')


class DefaultSecurity(uvcsite.Page):
    grok.title("DefaultSecurity")
    grok.context(IUVCSite)

    def render(self):
        return "hi"

class Table(TablePage):
    """
    """
    grok.context(IMyHomeFolder)
    grok.require('uvc.Allow')
    cssClasses = {'table': 'tablesorter'}
    grok.title('Tabelle')
    title = "Tabelle"
    description = "Beispieltabelle"
    #uvcsite.sectionmenu(uvcsite.IExtraViews)


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

class UAA(uvcsite.Altdaten):
    grok.context(uvcsite.IUVCSite)
    title = "HANS"

    @property
    def values(self):
        return []
