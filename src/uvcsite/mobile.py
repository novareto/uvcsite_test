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
    grok.view(LandingPage)
    grok.require('zope.Public')

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


class Login(BaseMobilePage):
    grok.layer(MobileLayer)
    grok.require('zope.Public')

import megrok.pagetemplate as pt
from dolmen.app.layout import Form as DAForm

class MobileFormTemplate(pt.PageTemplate):
    pt.view(DAForm)
    grok.layer(MobileLayer)


from dolmen.app.authentication.browser import login
class MobileLoginForm(login.Login):
    grok.name('mobileloginform')
    grok.layer(MobileLayer)


class LoginForm(MobilePage):
    grok.layer(MobileLayer)
    grok.context(uvcsite.IUVCSite)
    grok.view(Login)
    grok.require('zope.Public')

    def render(self):
        loginform = getMultiAdapter((self.context, self.request), name="mobileloginform")
        loginform.update()
        loginform.updateWidgets()
        return loginform.render()
