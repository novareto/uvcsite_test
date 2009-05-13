# -*- coding: utf-8 -*-

import grok
from zope.interface import Interface
from uvcsite.interfaces import *

class Headers(grok.ViewletManager):
    """ Viewlet Manager for the Header """
    grok.name('uvcsite.headers')
    grok.context(Interface)
    grok.implements(IHeaders)

class Toolbar(grok.ViewletManager):
    """ ViewletManager for the Toolbar """
    grok.name('uvcsite.toolbar')
    grok.context(Interface)
    grok.implements(IToolbar)

class GlobalMenu(grok.ViewletManager):
    grok.name('uvcsite.globalmenu')
    grok.context(Interface)
    grok.implements(IGlobalMenu)

class Sidebar(grok.ViewletManager):
    """ ViewletManager for the Sidebar """
    grok.name('uvcsite.sidebar')
    grok.context(Interface)
    grok.implements(ISidebar)

class Footer(grok.ViewletManager):
    """ ViewletManager for the Footer """
    grok.name('uvcsite.footer')
    grok.context(Interface)
    grok.implements(IFooter)

class Logo(grok.ViewletManager):
    """ ViewletManager for the LOGO """
    grok.name('uvcsite.logo')
    grok.context(Interface)
    grok.implements(ILogo)

class PersonalMenu(grok.ViewletManager):
    """ ViewletManager for the PersonalPropertiesPanel """
    grok.name('uvcsite.personalpanel')
    grok.context(Interface)
    grok.implements(IPersonalMenu)

class StatusMessage(grok.ViewletManager):
    """ ViewletManager for StatusMessages"""
    grok.name('uvcsite.statusmessage')
    grok.context(Interface)
    grok.implements(IStatusMessage)     
