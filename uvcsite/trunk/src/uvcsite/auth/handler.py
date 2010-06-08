# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
from interfaces import IUVCAuth, IMasterUser
from persistent import Persistent
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.app.authentication.httpplugins import HTTPBasicAuthCredentialsPlugin
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.authentication.principalfolder import PrincipalInfo, Principal
from zope.app.cache.ram import RAMCache
from zope.component import getUtility
from zope.interface import implements
from zope.location.interfaces import ILocation
from zope.security.interfaces import IPrincipal
from zope.app.authentication.session import SessionCredentialsPlugin
from zope.app.authentication.interfaces import ICredentialsPlugin

from grokcore import message

authCache = RAMCache()


@grok.adapter(IPrincipal)
@grok.implementer(IMasterUser)
def masteruser(self):
    """Return always the Master User"""
    if not "-" in self.id:
        return self
    master_id = self.id.split('-')[0]
    return Principal(master_id)


def setup_pau(pau):
    """ this set´s up the pluggable authentication utility"""
    pau['principals'] = UVCAuthenticator('contact.principals.')
    pau.authenticatorPlugins = ['principals']
    #pau['basic'] = HTTPBasicAuthCredentialsPlugin()
    pau.credentialsPlugins = ['credentials']


class MySessionCredentialsPlugin(grok.GlobalUtility, SessionCredentialsPlugin):
    grok.provides(ICredentialsPlugin)
    grok.name('credentials')

    loginpagename = 'login'
    loginfield = 'widgets.login'
    passwordfield = 'widgets.password'


class UVCAuthenticator(grok.LocalUtility):
    """ Custom Authenticator for UVC-Site"""
    grok.implements(IAuthenticatorPlugin)
    grok.name('principals')

    def __init__(self, prefix=u''):
        self.prefix = prefix

    def authenticateCredentials(self, credentials):
        """check if username and password match
           get the credentials from the IUserManagement Utility"""
        if not (credentials and 'login' in credentials
                and 'password' in credentials):
            return
        login, password = credentials['login'], credentials['password']
        key = dict(login=login, password=password)
        user = authCache.query(self, key)
#        if getattr(utility, 'pw_hash', False):
#            password = utility.pw_hash(password)
        if not user:
            utility = getUtility(IUserManagement)
            user = utility.getUser(login)
            authCache.set(user, self, key)
        if not user:
            return
        if password != user.get('passwort'):
            return
        return PrincipalInfo(login, login, login, login)

    def principalInfo(self, id):
        """we don´t need this method"""
        return None
