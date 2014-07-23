# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from uvc.api import api
from uvc.homefolder.interfaces import IHomefolders
from uvclight.interfaces import IUserLoggedInEvent
from uvcsite.content.folderinit import createProductFolders
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.component import getUtility
from zope.securitypolicy.interfaces import IPrincipalRoleManager
import uvcsite


@api.subscribe(IUserLoggedInEvent)
def applyPermissionsForExistentCoUsers(factory):
    principal = factory.principal
    createProductFolders(principal)
    homefolders = getUtility(IHomefolders)
    homefolder = homefolders.get(principal.id)
    if homefolder is None:
        homefolder = homefolders.assign_homefolder(principal.id)
        return
    um = getUtility(IUserManagement)
    rollen = um.getUser(principal.id)['rollen']
    if homefolder.__name__ != principal.id:
        for pf in homefolder.keys():
            if pf in rollen:
                prm = IPrincipalRoleManager(homefolder.get(pf))
                if prm.getSetting('uvc.Editor', principal.id).getName() == 'Unset':
                    prm.assignRoleToPrincipal('uvc.Editor', principal.id)
                    uvcsite.log('Give uvc.Editor to %s in folder %s' % (principal.id, pf))


## @uvclight.subscribe(IAuthenticatedPrincipalCreated)
## def applyGroups(factory):
##     principal = factory.principal
##     principal.groups.append('uvc.Member')
