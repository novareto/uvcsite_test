# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


## import uvclight
## import uvcsite

## from uvcsite.extranetmembership.interfaces import IUserManagement
## from zope.component import getUtility
## from dolmen.authentication.events import IUserLoggedInEvent
## from zope.securitypolicy.interfaces import IPrincipalRoleManager
## from uvcsite.content.folderinit import createProductFolders


## @uvclight.subscribe(IUserLoggedInEvent)
## def applyPermissionsForExistentCoUsers(factory):
##     principal = factory.object
##     createProductFolders(principal)
##     homefolder = IHomeFolder(principal).homeFolder
##     if not homefolder:
##         return
##     um = getUtility(IUserManagement)
##     rollen = um.getUser(principal.id)['rollen']
##     if homefolder.__name__ != principal.id:
##         for pf in homefolder.keys():
##             if pf in rollen:
##                 prm = IPrincipalRoleManager(homefolder.get(pf))
##                 if prm.getSetting('uvc.Editor', principal.id).getName() == 'Unset':
##                     prm.assignRoleToPrincipal('uvc.Editor', principal.id)
##                     uvcsite.log('Give uvc.Editor to %s in folder %s' % (principal.id, pf))


## @uvclight.subscribe(IAuthenticatedPrincipalCreated)
## def applyGroups(factory):
##     principal = factory.principal
##     principal.groups.append('uvc.Member')
