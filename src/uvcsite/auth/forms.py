# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


import grok
import uvcsite

from zope import schema
from zope import component
from zope.interface import Interface

from z3c.form.interfaces import HIDDEN_MODE
from megrok.z3cform.base import PageForm, Fields, button

from zope.app.security.interfaces import IAuthentication, IUnauthenticatedPrincipal, ILogout

class ILoginForm(Interface):
    login = schema.BytesLine(title=u'Mitgliedsnummer', required=True)
    camefrom = schema.BytesLine(title=u'', required=False)
    password = schema.Password(title=u'Passwort', required=True)


class Login(PageForm):
    grok.context(Interface)
    grok.require('zope.Public')
    label = "Herzlich Willkommen im Extranet"
    description = u"In diesem Bereich können Sie verschiedene Application nutzten! "

    prefix = ''
    fields = Fields(ILoginForm)
    ignoreContext = True

    def updateWidgets(self):
        super(Login, self).updateWidgets()
        self.widgets['camefrom'].mode = HIDDEN_MODE

    @button.buttonAndHandler(u'login', name="login")
    def handle_login(self, action):
        self.redirect(self.request.form.get('camefrom', self.url(grok.getSite())))


class Logout(uvcsite.Page): 
    grok.context(Interface) 
    grok.require('zope.Public') 
 
    def update(self): 
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal): 
            auth = component.getUtility(IAuthentication) 
            ILogout(auth).logout(self.request) 

    def render(self):
        return "Sie Sind Jetzt Ausgeloggt"
