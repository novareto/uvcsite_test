# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

## import uvcsite
## import zope.security
## import xmlrpclib
## from grokcore import message
## from persistent import Persistent
## from zope.component import getUtility
## from zope.interface import implements, Interface
## from zope.schema import ASCIILine
## from zope.session.interfaces import ISession
## from zope.location.interfaces import ILocation
## from zope.security.interfaces import IPrincipal
## from zope.securitypolicy.interfaces import IPrincipalRoleManager
## from zope.securitypolicy.settings import Allow

## from zope.pluggableauth.factories import PrincipalInfo, Principal
## from zope.pluggableauth.interfaces import IAuthenticatorPlugin
## from zope.pluggableauth.interfaces import ICredentialsPlugin
## from zope.pluggableauth.plugins.session import SessionCredentialsPlugin

## from interfaces import IUVCAuth, IMasterUser
## from uvcsite.extranetmembership.interfaces import IUserManagement

## from dolmen.authentication import UserLoginEvent
## from zope.event import notify

## USER_SESSION_KEY = "uvcsite.authentication"


## @grok.adapter(IPrincipal)
## @grok.implementer(IMasterUser)
## def masteruser(self):
##     """Return always the Master User"""
##     if not "-" in self.id:
##         return self
##     master_id = self.id.split('-')[0]
##     return Principal(master_id)


## class CheckRemote(grok.XMLRPC):
##     grok.context(uvcsite.IUVCSite)

##     def checkAuth(self, user, password):
##         if isinstance(user, xmlrpclib.Binary):
##             user = unicode(user.data)
##         if isinstance(password, xmlrpclib.Binary):
##             password = unicode(password.data)

##         plugin = getUtility(IAuthenticatorPlugin, 'principals')
##         principal = plugin.authenticateCredentials(dict(
##             login=user,
##             password=password))
##         if principal:
##             notify(UserLoginEvent(Principal(user)))
##             return 1
##         return 0

##     def getRemoteDashboard(self, user):
##        return (u"<ul><li><a href='%(url)s/link1'>Uvcsite link1</a></li>" +
##                u"<li><a href='%(url)s/link2'>Uvcsite link2</a></li></ul>")
        
##     def getRoles(self, user):
##         manager = IPrincipalRoleManager(self.context)
##         setting = manager.getRolesForPrincipal(user)
##         return [role[0] for role in setting if role[1] is Allow]
