# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
import zope.security

from grokcore import message
from persistent import Persistent
from zope.component import getUtility
from zope.interface import implements, Interface
from zope.schema import ASCIILine
from zope.session.interfaces import ISession
from zope.location.interfaces import ILocation
from zope.security.interfaces import IPrincipal

from zope.pluggableauth.factories import PrincipalInfo, Principal
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.pluggableauth.interfaces import ICredentialsPlugin
from zope.pluggableauth.plugins.session import SessionCredentialsPlugin

from interfaces import IUVCAuth, IMasterUser
from uvcsite.extranetmembership.interfaces import IUserManagement, IAdHocUserManagement

from dolmen.authentication import UserLoginEvent
from zope.event import notify

USER_SESSION_KEY = "uvcsite.authentication"


@grok.adapter(IPrincipal)
@grok.implementer(IMasterUser)
def masteruser(self):
    """Return always the Master User"""
    if not "-" in self.id:
        return self
    master_id = self.id.split('-')[0]
    return Principal(master_id)


class UVCAuthenticator(grok.Model):
    """ Custom Authenticator for UVC-Site"""
    grok.implements(IAuthenticatorPlugin)
    prefix = 'contact.principals.'

    def isAdHocUser(self, login):
        """ 
        Returns True if the User is a AdHoc-User
        """
        if login.startswith('A'):
            return True
        return False

    def authenticateCredentials(self, credentials):
        """
        Check if username and password match
        get the credentials from the IUserManagement Utility
        """
        request = zope.security.management.getInteraction().participations[0]
        session = ISession(request)['uvcsite.authentication']
        authenticated = session.get(USER_SESSION_KEY)
        if authenticated is None:
            if not (credentials and 'login' in credentials
                    and 'password' in credentials):
                return
            login, password = credentials['login'], credentials['password']

            if self.isAdHocUser(login):
                utility = getUtility(IAdHocUserManagement)
            else:
                utility = getUtility(IUserManagement)

            if not utility.checkRule(login):
                return 

            user = utility.getUser(login)
            if not user:
                return

            if hasattr(utility, 'checkPW'):
                if not utility.checkPW(password, user.get('passwort')):
                    return
            else:
                if password != user.get('passwort'):
                    return
            user_id = login
            #if self.isAdHocUser(login):
            #    user_id = user.get('mnr')
            authenticated = session[USER_SESSION_KEY] = dict(
                id = user_id,
                title = login,
                description = login,
                login = login)
        return PrincipalInfo(**authenticated)

    def principalInfo(self, id):
        """we don´t need this method"""
        if id.startswith('uvc.'):
            return PrincipalInfo(id, id, id, id)


class CheckRemote(grok.XMLRPC):
    grok.context(uvcsite.IUVCSite)

    def checkAuth(self, user, password):
        plugin = getUtility(IAuthenticatorPlugin, 'principals')
        principal = plugin.authenticateCredentials(dict(
            login=user,
            password=password))
        if principal:
            notify(UserLoginEvent(Principal(user)))
            return 1
        return 0
