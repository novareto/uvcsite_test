# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from uvcsite import PersonalPreferences, GlobalMenu, PersonalMenu

from zope.app.homefolder.interfaces import IHomeFolder

from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IUnauthenticatedPrincipal


class UserName(uvcsite.MenuItem):
    grok.title("USERSNAME")
    grok.context(Interface)
    grok.viewletmanager(uvcsite.IPersonalPreferences)
    grok.order(10)
    grok.require('zope.View')


class MeinOrdner(uvcsite.MenuItem):
    grok.context(Interface)
    grok.name('Mein Ordner')
    grok.title('Mein Ordner')
    grok.viewletmanager(uvcsite.IPersonalPreferences)
    grok.order(20)
    grok.require('zope.View')

    @property
    def hfurl(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal).homeFolder
        return absoluteURL(homeFolder, self.request)

    @property
    def action(self):
        return self.hfurl


class Mitbenutzerverwaltung(uvcsite.MenuItem):
    grok.context(uvcsite.IMyHomeFolder)
    grok.name('Mitbenutzerverwaltung')
    grok.title('Mitbenutzerverwaltung')
    grok.viewletmanager(uvcsite.IPersonalMenu)
    grok.order(30)
    grok.require('uvc.ManageCoUsers')

    @property
    def url(self):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal).homeFolder
        return absoluteURL(homeFolder, self.request) + '/enms'

    @property
    def action(self):
        return self.url
