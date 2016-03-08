#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok
import uvcsite
from uvcsite.extranetmembership.interfaces import IUserManagement


class UserManagement(grok.GlobalUtility):
    """ Utility for Usermanagement """
    grok.implements(IUserManagement)
    users = (
        {'mnr':'0101010001', 'az': '00', 'passwort':'passwort', 'email':'ck@novareto.de', 'rollen':['Adressbook']},
        {'mnr':'0202020002', 'az': '00', 'passwort':'passwort', 'email':'test@test.de', 'rollen':[]},
        {'mnr':'0101010001-q', 'az': '-q', 'passwort':'passwort', 'email':'test@test.de', 'rollen':['Adressbook']},
        {'mnr':'0101010001', 'az': '01', 'passwort':'passwort', 'email':'ck1@novareto.de', 'rollen':['Adressbook']},
        {'mnr':'0101010001', 'az': '02', 'passwort':'passwort', 'email':'test@test.de', 'rollen':[]},
        {'mnr':'0101010002', 'az': '02', 'passwort':'passwort', 'email':'test@test.de'},
        {'mnr':'0101010002', 'az': '03', 'passwort':'passwort', 'email':'test@test.de'},
        {'mnr':'lars', 'az': '00', 'passwort':'passwort', 'email':'test@test.de', 'rollen':[]},
        )

    def updUser(self, **kwargs):
        """Updates a User"""

    def deleteUser(self, mnr):
        """Delete the User"""

    def addUser(self, **kwargs):
        """Adds a User"""

    def zerlegUser(self, mnr):
        ll = mnr.split('-')
        if len(ll) == 1:
            return mnr, '00'
        return ll

    def getUser(self, mnr):
        """Return a User"""
        mnr, az = self.zerlegUser(mnr)
        from copy import deepcopy
        for user in deepcopy(self.users):
            if user.get('mnr') == mnr and user.get('az') == az:
                return user
        return None

    def getUserByEMail(self, mail):
        from copy import deepcopy
        for user in deepcopy(self.users):
            if user.get('email') == mail:
                return user
        return None

    def getUserGroups(self, mnr):
        """Return a group of Users"""
        ret = []
        from copy import deepcopy
        for x in deepcopy(self.users):
            usr = "%s-%s" % (x['mnr'], x['az'])
            ret.append(dict(cn=usr, mnr=usr, rollen=x.get('rollen', []), az=x.get('az')))
        return ret

    def updatePasswort(self, **kwargs):
        """Change a passwort from a user"""

    def checkRule(self, login):
        uvcsite.log(login)
        return True



from uvcsite.interfaces import IMyHomeFolder
from zope import interface
from zope.securitypolicy.interfaces import Allow
from dolmen.security.policies.principalrole import ExtraRoleMap
from zope.securitypolicy.zopepolicy import settingsForObject
from zope.securitypolicy.securitymap import SecurityMap
from zope.securitypolicy.interfaces import (
     IPrincipalRoleManager, IPrincipalRoleMap, IRolePermissionMap)




class ViewPermission(grok.View):
    grok.context(interface.Interface)

    def render(self):
        context = self.context
        print settingsForObject(context)


#from uvcsite.tests.simpleaddon import IAdressBook
#class QuickUserRoleManager(ExtraRoleMap):
#    grok.implements(IPrincipalRoleManager, IPrincipalRoleMap)
#
#    def _compute_extra_data(self):
#        extra_map = SecurityMap()
#        extra_map.addCell('uvc.Editor', self.context.__parent__.__name__ + '-q', Allow)
#        return extra_map
#
#from grokcore.component import global_adapter
#global_adapter(QuickUserRoleManager, (IAdressBook,), IPrincipalRoleMap)
#global_adapter(QuickUserRoleManager, (IAdressBook,), IPrincipalRoleManager)

from zope.pluggableauth.factories import Principal, AuthenticatedPrincipalFactory
from uvc.tbskin.skin import ITBSkinLayer
from zope.pluggableauth.interfaces import IPrincipalInfo, AuthenticatedPrincipalCreated


class UVCPrincipal(Principal):

    foo = u"bar"


class MyOwnPrincpalFactory(AuthenticatedPrincipalFactory, grok.MultiAdapter):
    grok.adapts(IPrincipalInfo, ITBSkinLayer)

    def __call__(self, authentication):
        principal = UVCPrincipal(authentication.prefix + self.info.id,
                              self.info.title,
                              self.info.description)
        grok.notify(AuthenticatedPrincipalCreated(
            authentication, principal, self.info, self.request))
        return principal

