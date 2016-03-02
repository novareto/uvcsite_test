# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


import grok
import uvcsite

from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.pluggableauth.interfaces import IAuthenticatedPrincipalCreated
from zope.app.homefolder.interfaces import IHomeFolder
from zope.component import getUtility
from dolmen.authentication.events import IUserLoggedInEvent
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from uvcsite.content.folderinit import createProductFolders
from uvcsite.auth.interfaces import ICOUser
from zope.interface import alsoProvides


@grok.subscribe(IUserLoggedInEvent)
def applyPermissionsForExistentCoUsers(factory):
    principal = factory.object
    createProductFolders(principal)
    homefolder = IHomeFolder(principal).homeFolder
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
    alsoProvides(principal, ICOUser)
