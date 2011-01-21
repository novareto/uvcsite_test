#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok
import uvcsite
from uvcsite.extranetmembership.interfaces import IUserManagement

users = [
    {'mnr':'0101010001', 'passwort':'passwort', 'email':'test@test.de', 'rollen':['addressbook']},
    {'mnr':'0101010001-q', 'passwort':'passwort', 'email':'test@test.de', 'rollen':['addressbook']},
    {'mnr':'0101010002', 'passwort':'passwort', 'email':'test@test.de'},
    ]


class UserManagement(grok.GlobalUtility):
    """ Utility for Usermanagement """
    grok.implements(IUserManagement)

    def updUser(self, **kwargs):
        """Updates a User"""

    def deleteUser(self, mnr):
        """Delete the User"""

    def addUser(self, **kwargs):
        """Adds a User"""

    def getUser(self, mnr):
        """Return a User"""
        for user in users:
            if user.get('mnr') == mnr:
                return user
        return None

    def getUserGroups(self, mnr):
        """Return a group of Users"""
        return users

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
