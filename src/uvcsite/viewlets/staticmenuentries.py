# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok

from uvcsite.interfaces import IPersonalPreferences
from uvc.layout.menus import PersonalPreferences

from dolmen.menu import menu, menuentry, Entry
from zope.app.homefolder.interfaces import IHomeFolder

from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IUnauthenticatedPrincipal


class UserName(Entry):
    grok.name('myname')
    grok.context(Interface)
    menu(PersonalPreferences)
    grok.order(10)

    def render(self):
        return '<a href="#"> %s </a>' % self.request.principal.description or self.request.principal.id


class MeinOrdner(Entry):
    grok.context(Interface)
    grok.name('Mein Ordner')
    grok.title('Mein Ordner')
    menu(PersonalPreferences)
    grok.order(20)

    @property
    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal).homeFolder
        return absoluteURL(homeFolder, self.request)


class Mitbenutzerverwaltung(Entry):
    grok.context(Interface)
    grok.name('Mitbenutzerverwaltung')
    grok.title('Mitbenutzerverwaltung')
    menu(PersonalPreferences)
    grok.order(30)

    @property
    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal).homeFolder
        return absoluteURL(homeFolder, self.request) + '/enms'


class Logout(Entry):
    grok.name('Abmelden')
    grok.context(Interface)
    menu(PersonalPreferences)
    grok.order(40)

    @property
    def url(self):
        return "https://www.google.de"
