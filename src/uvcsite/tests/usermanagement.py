#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok
import uvcsite
from uvcsite.extranetmembership.interfaces import IUserManagement


class UserManagement(grok.GlobalUtility):
    """ Utility for Usermanagement """
    grok.implements(IUserManagement)
    users = ( 
        {'mnr':'0101010001', 'az': '00', 'passwort':'passwort', 'email':'test@test.de', 'rollen':['addressbook']},
        {'mnr':'0101010001-q', 'az': '-q', 'passwort':'passwort', 'email':'test@test.de', 'rollen':['addressbook']},
        {'mnr':'0101010001', 'az': '01', 'passwort':'passwort', 'email':'test@test.de'},
        {'mnr':'0101010002', 'az': '02', 'passwort':'passwort', 'email':'test@test.de'},
        {'mnr':'0101010002', 'az': '03', 'passwort':'passwort', 'email':'test@test.de'},
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
        for user in self.users:
            if user.get('mnr') == mnr and user.get('az') == az:
                return user
        return None

    def getUserGroups(self, mnr):
        """Return a group of Users"""
        return self.users

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
