# -*- coding: utf-8 -*-

import grok

from uvcsite import uvcsiteMF as _
from zope.interface import Interface
from zope.component import getUtility
from z3c.menu.simple.menu import GlobalMenuItem
from uvcsite.interfaces import IGlobalMenu, IPersonalMenu, IPersonalPreferences
from uvcsite.viewlets.utils import MenuItem
from zope.app.homefolder.interfaces import IHomeFolder
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.app import zapi
from uvcsite.api.interfaces import ICompanyInfo

class MyName(grok.Viewlet):
    grok.name('myname')
    grok.context(Interface)
    grok.viewletmanager(IPersonalPreferences)
    grok.order(1)

    css = "blue"

    def render(self):
	html = "<span> %s </span> " %self.request.principal.description
	return html

class MyFolder(MenuItem):
    grok.name(_(u'Mein Ordner'))
    grok.context(Interface)
    grok.viewletmanager(IPersonalPreferences)
    grok.order(2)

    @property
    def urlEndings(self):
	principal = self.request.principal
        return str(principal.id)

    @property
    def url(self):
	principal = self.request.principal
	if IUnauthenticatedPrincipal.providedBy(principal):
	    return 
	homeFolder = IHomeFolder(principal).homeFolder
        return zapi.absoluteURL(homeFolder, self.request)


class Logout(MenuItem):
    grok.name(_(u'ausloggen'))
    grok.context(Interface)
    grok.viewletmanager(IPersonalPreferences)
    grok.order(9)

    urlEndings = "ausloggen"
    viewURL = "https://XXX/login/logout"
    
    #@property
    #def view(self):
    #    return "http://www.google.de"


class PersonalProperties(MenuItem):
    grok.name(_(u'Meine Einstellungen'))
    grok.context(Interface)
    grok.viewletmanager(IPersonalPreferences)
    grok.order(2)

    title= _(u'Meine Einstellungen')
    urlEndings = "personalpanelview"
    viewURL = "personalpanelview"



class ChangePassword(MenuItem):
    grok.name(_(u'Passwort'))
    grok.context(Interface)
    grok.viewletmanager(IPersonalMenu)
    grok.order(1)

    urlEndings = "changepassword"
    viewURL = "changepassword"

