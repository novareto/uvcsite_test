# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok

from uvcsite import log
from uvcsite.homefolder.interfaces import IHomeFolder
from dolmen.authentication.events import IUserLoggedInEvent
from zope.securitypolicy.interfaces import IPrincipalRoleManager


class AccessHomeFolder(grok.Permission):
    grok.name('uvc.AccessHomeFolder')


class HomeFolderUser(grok.Role):
    grok.name('uvc.HomeFolderUser')
    grok.permissions('uvc.AccessHomeFolder', )


@grok.subscribe(IUserLoggedInEvent)
def applyViewContentForCoUsers(factory):
    principal = factory.object
    homefolder = IHomeFolder(principal).homeFolder
    if not homefolder:
        return
    if homefolder.__name__ != principal.id:
        hprm = IPrincipalRoleManager(homefolder)
        if hprm.getSetting('uvc.HomeFolderUser', principal.id).getName() in ('Deny', 'Unset'):
            hprm.assignRoleToPrincipal('uvc.HomeFolderUser', principal.id)
            log('applying Role uvc.HomeFolderUser for USER %s in HOMEFOLDER %s' % (principal.id, homefolder.__name__))
