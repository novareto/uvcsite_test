# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope import interface
from megrok import layout
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.component import getMultiAdapter


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


class BaseMobilePage(layout.Page):
    grok.layer(MobileLayer)
    grok.require('zope.Public')
    grok.context(uvcsite.IUVCSite)
    macro = "mobilemacros"

    def getMacro(self, name):
        mm = getMultiAdapter((self.context, self.request), name=self.macro)
        return mm.macros[name]


class LandingPage(BaseMobilePage):
    grok.name('index')


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
    grok.require('zope.Public')


class MobilePage(grok.Viewlet):
    grok.baseclass()
    grok.layer(MobileLayer)
    grok.viewletmanager(IMobilePagesManager)
    grok.require('zope.Public')
    grok.view(LandingPage)

    @property
    def id(self):
        return grok.name.bind().get(self)

    @property
    def title(self):
        return grok.title.bind().get(self)


class MobileMacros(grok.View):
    grok.layer(MobileLayer)
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')
