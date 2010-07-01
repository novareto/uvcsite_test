# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import zope.security

from interfaces import IUVCAuth, IMasterUser
from persistent import Persistent
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.app.authentication.httpplugins import HTTPBasicAuthCredentialsPlugin
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.authentication.principalfolder import PrincipalInfo, Principal
from zope.component import getUtility
from zope.interface import implements
from zope.location.interfaces import ILocation
from zope.security.interfaces import IPrincipal
from zope.app.authentication.session import SessionCredentialsPlugin
from zope.app.authentication.interfaces import ICredentialsPlugin
from zope.session.interfaces import ISession

from grokcore import message

USER_SESSION_KEY = "uvcsite.authentication"


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
        request = zope.security.management.getInteraction().participations[0]   
        session = ISession(request)['uvcsite.authentication']

        authenticated = session.get(USER_SESSION_KEY)
        if authenticated is None:
            if not (credentials and 'login' in credentials
                    and 'password' in credentials):
                return
            login, password = credentials['login'], credentials['password']
            utility = getUtility(IUserManagement)
            user = utility.getUser(login)
            if not user:
                return
            if password != user.get('passwort'):
                return
            authenticated = session[USER_SESSION_KEY] = dict(
                id = login,
                title = login,
                description = login,
                login = login)
        return PrincipalInfo(**authenticated)

    def principalInfo(self, id):
        """we don´t need this method"""
        return None
