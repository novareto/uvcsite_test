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


@grok.subscribe(IUserLoggedInEvent)
def applyPermissionsForExistentCoUsers(factory):
    principal = factory.object
    homefolder = IHomeFolder(principal).homeFolder
    um = getUtility(IUserManagement)
    import pdb; pdb.set_trace() 
    for user in um.getUser(principal.id)['rollen']:
        pass
