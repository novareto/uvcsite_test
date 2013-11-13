# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


import grok
import uvcsite

from uvc.homefolder import IHomefolder
from dolmen.authentication.events import IUserLoggedInEvent
from uvcsite.content.folderinit import createProductFolders
from uvcsite.extranetmembership.interfaces import IUserManagement
from uvcsite.utils.shorties import getHomeFolder
from zope.component import getUtility
from zope.pluggableauth.interfaces import IAuthenticatedPrincipalCreated
from zope.securitypolicy.interfaces import IPrincipalRoleManager


@grok.subscribe(IUserLoggedInEvent)
def applyPermissionsForExistentCoUsers(factory):
    principal = factory.object
    createProductFolders(principal)
    homefolder = IHomefolder(principal)
    if not homefolder:
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


@grok.subscribe(IAuthenticatedPrincipalCreated)
def applyGroups(factory):
    principal = factory.principal
    principal.groups.append('uvc.Member')
