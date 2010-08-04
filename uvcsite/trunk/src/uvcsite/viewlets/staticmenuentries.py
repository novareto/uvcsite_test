# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from uvc.layout.menus import PersonalPreferences, GlobalMenu, PersonalMenu

from megrok import navigation
from zope.app.homefolder.interfaces import IHomeFolder

from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IUnauthenticatedPrincipal


class UserName(grok.View):
    grok.title("USERSNAME")
    grok.context(Interface)
    grok.viewletmanager(uvcsite.IPersonalPreferences)
    grok.order(10)

    def render(self):
        return '<a href="#"> %s </a>' % self.request.principal.description or self.request.principal.id


class MeinOrdner(grok.View):
    grok.context(Interface)
    grok.name('Mein Ordner')
    grok.title('Mein Ordner')
    navigation.sitemenuitem(uvcsite.IPersonalPreferences)
    grok.order(20)

    @property
    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal).homeFolder
        return absoluteURL(homeFolder, self.request)

    def render(self):
        return self.response.redirect(self.url)


class Mitbenutzerverwaltung(grok.View):
    grok.context(Interface)
    grok.name('Mitbenutzerverwaltung')
    grok.title('Mitbenutzerverwaltung')
    navigation.sitemenuitem(uvcsite.IPersonalMenu)
    grok.order(30)

    @property
    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal).homeFolder
        return absoluteURL(homeFolder, self.request) + '/enms'

    def render(self):
        return self.response.redirect(self.url)
