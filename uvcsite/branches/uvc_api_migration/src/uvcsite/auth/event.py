# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import uvclight
import uvcsite

from uvc.api import api
from uvc.homefolder.interfaces import IHomefolders
from uvcsite.content.folderinit import createProductFolders
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.component import getUtility
from zope.securitypolicy.interfaces import IPrincipalRoleManager


@api.subscribe(uvclight.IUserLoggedInEvent)
def applyPermissionsForExistentCoUsers(factory):
    user = factory.principal
    homefolders = getUtility(IHomefolders)
    homefolder = homefolders.get(user.id)
    if homefolder is None:
        homefolder = homefolders.assign_homefolder(user.id)
        return
    createProductFolders(user)
    um = getUtility(IUserManagement)
    rollen = um.getUser(user.id)['rollen']
    if homefolder.__name__ != user.id:
        for pf in homefolder.keys():
            if pf in rollen:
                prm = IPrincipalRoleManager(homefolder.get(pf))
                if prm.getSetting('uvc.Editor', user.id).getName() == 'Unset':
                    prm.assignRoleToUser('uvc.Editor', user.id)
                    uvcsite.log(
                        'Give uvc.Editor to %s in folder %s' % (user.id, pf))
