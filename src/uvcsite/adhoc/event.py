# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from dolmen.authentication.events import IUserLoggedInEvent
from interfaces import IAdHocPrincipal, IAdHocUserInfo
from zope.app.homefolder.interfaces import IHomeFolder
from zope.interface import alsoProvides
from zope.pluggableauth.interfaces import IAuthenticatedPrincipalCreated
from uvcsite.adhoc.components import AdHocFolder


@grok.subscribe(IAuthenticatedPrincipalCreated)
def mark_adhocuser(factory):
    principal = factory.principal
    ahui = IAdHocUserInfo(principal)
    if ahui.isAdHocUser:
        alsoProvides(principal, IAdHocPrincipal)
        principal.groups.append('uvc.AdHocGroup')


@grok.subscribe(IUserLoggedInEvent)
def create_adhoc_folder(factory):
    principal = factory.object
    if IAdHocUserInfo(principal).isAdHocUser:
        homefolder = IHomeFolder(principal).homeFolder
        if 'adhoc' not in homefolder:
            homefolder['adhoc'] = AdHocFolder()
            uvcsite.log('Added the adhoc Folder to homefolder %s.' % homefolder.__name__)

