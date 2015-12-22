# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
import xmlrpclib
import zope.security
import xmlrpclib
from zope.component import getUtility
from zope.session.interfaces import ISession
from zope.security.interfaces import IPrincipal
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.settings import Allow

from zope.pluggableauth.factories import PrincipalInfo, Principal
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from interfaces import IMasterUser
from uvcsite.extranetmembership.interfaces import IUserManagement

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

            utility = getUtility(IUserManagement)

            if hasattr(utility, 'changeLogin'):
                login = utility.changeLogin(login)

            if not utility.checkRule(login):
                return
            if '@' in login:
                user = utility.getUserByEMail(login)
            else:
                user = utility.getUser(login)
            if not user:
                return

            if hasattr(utility, 'checkPW'):
                if not utility.checkPW(password, user.get('passwort')):
                    return
            else:
                if password != user.get('passwort'):
                    return
            user_id = user['mnr']
            if user['az'] != '00':
                user_id = "%s-%s" % (user['mnr'], user['az'])

            authenticated = session[USER_SESSION_KEY] = dict(
                id=user_id,
                title=login,
                description=login,
                login=login)
        return PrincipalInfo(**authenticated)

    def principalInfo(self, id):
        """we don´t need this method"""
        if id.startswith('uvc.'):
            return PrincipalInfo(id, id, id, id)


class CheckRemote(grok.XMLRPC):
    grok.context(uvcsite.IUVCSite)

    def checkAuth(self, user, password):
        if isinstance(user, xmlrpclib.Binary):
            user = unicode(user.data)
        if isinstance(password, xmlrpclib.Binary):
            password = unicode(password.data)
        plugin = getUtility(IAuthenticatorPlugin, 'principals')
        principal = plugin.authenticateCredentials(dict(
            login=user,
            password=password))
        if principal:
            notify(UserLoginEvent(Principal(user)))
            return 1
        return 0

    def getRemoteDashboard(self, user):
       return (u"<ul><li><a href='%(url)s/link1'>Uvcsite link1</a></li>" +
               u"<li><a href='%(url)s/link2'>Uvcsite link2</a></li></ul>")

    def getRoles(self, user):
        manager = IPrincipalRoleManager(self.context)
        setting = manager.getRolesForPrincipal(user)
        return [role[0] for role in setting if role[1] is Allow]
