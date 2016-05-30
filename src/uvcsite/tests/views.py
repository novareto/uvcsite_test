# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from zope.interface import Interface
from uvcsite.interfaces import IMyHomeFolder, IUVCSite, IDocumentActions
from megrok.z3ctable import TablePage, Column, table
import uvcsite
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from uvc.layout.slots.interfaces import IRenderable
from grokcore.chameleon.components import ChameleonPageTemplateFile


class PDF(uvcsite.MenuItem):
    grok.viewletmanager(IDocumentActions)
    grok.name('pdf')
    icon = "glyphicon glyphicon-paperclip"
    action = "/index"

    def update(self):
        self.view.flash(u'I am a Message', type="success")


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


from uvc.layout.slots.interfaces import IRenderable
class RenderableItem(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(uvcsite.IGlobalMenu)
    grok.implements(IRenderable)

    def render(self):
        return "<li> <a href=''> HALLO WELT </a> </li>"


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
    cssClasses = {'td': 'right'}

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


from uvc.api import api

class MyTT(api.Page):
    api.context(uvcsite.IUVCSite)
    import pdb; pdb.set_trace() 
    template = api.get_template('test.cpt', __file__)

