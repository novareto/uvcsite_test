# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from zope import interface
from megrok import layout
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


grok.templatedir('templates')


class IMobileLayer(IDefaultBrowserLayer):
    pass


class MobileLayer(IMobileLayer):
    grok.skin('mobile')


class MobileLayout(layout.Layout):
    """ Base Layout for JQuery Mobile Applications
    """
    grok.context(interface.Interface)
    grok.layer(MobileLayer)


class LandingPage(layout.Page):
    grok.name('index')
    grok.layer(MobileLayer)
    grok.context(uvcsite.IUVCSite)


class IMobilePagesManager(interface.Interface):
    """ Marker Interface for Mobile Pages
    """


class MobilePagesManager(grok.ViewletManager):
    """ This Manager collects all Mobile Pages
    """
    grok.layer(MobileLayer)
    grok.context(uvcsite.IUVCSite)
    grok.name('uvc.mobilepagesmanager')
    grok.implements(IMobilePagesManager)


class MobilePage(grok.Viewlet):
    grok.baseclass()
    grok.layer(MobileLayer)
    grok.viewletmanager(IMobilePagesManager)


class MobileMacros(grok.View):
    grok.layer(MobileLayer)
    grok.context(uvcsite.IUVCSite)
