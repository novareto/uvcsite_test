# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


import grok
import uvcsite

from zope import schema
from zope import component
from zope.interface import Interface

from zeam.form import base
from dolmen.forms.base import Fields

from zope.app.security.interfaces import IAuthentication, IUnauthenticatedPrincipal, ILogout
from zope.session.interfaces import ISession

class ILoginForm(Interface):
    login = schema.BytesLine(title=u'Mitgliedsnummer', required=True)
    password = schema.Password(title=u'Passwort', required=True)
    camefrom = schema.BytesLine(title=u'camefrom', required=False)


class Login(uvcsite.Form):
    grok.context(Interface)
    grok.require('zope.Public')
    label = "Herzlich Willkommen im Extranet"
    description = u"In diesem Bereich können Sie verschiedene Online-Dienste nutzen! "

    fields = Fields(ILoginForm)
    fields['camefrom'].mode = "hidden"

    @base.action(u'Anmelden')
    def handle_login(self):
        data, errors = self.extractData()
        if errors:
            self.flash(u'Bitte korrigieren Sie Ihre Eingaben', type="error")
            return
        self.redirect(self.request.form.get('camefrom', self.url(grok.getSite())))


class Logout(uvcsite.Page): 
    grok.context(Interface) 
    grok.require('zope.Public') 
 
    def update(self): 
        session = ISession(self.request)
        session.delete()

    def render(self):
        return "Sie Sind jetzt ausgeloggt"
