# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from dolmen.authentication.events import IUserLoggedInEvent
from hurry.workflow.interfaces import IWorkflowTransitionEvent
from interfaces import IAdHocPrincipal, IAdHocUserInfo
from uvcsite.adhoc.components import AdHocFolder
from uvcsite.adhoc.interfaces import IAdHocFolder
from uvcsite.workflow.basic_workflow import PUBLISHED
from zope.app.homefolder.interfaces import IHomeFolder
from zope.interface import alsoProvides
from zope.pluggableauth.interfaces import IAuthenticatedPrincipalCreated
from zope.securitypolicy.interfaces import IPrincipalPermissionManager


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


@grok.subscribe(IWorkflowTransitionEvent)
def set_permissions(event):
    if event.destination != PUBLISHED:
        return
    object = event.object
    folder = object.__parent__
    if IAdHocFolder.providedBy(folder):
        ppm = IPrincipalPermissionManager(object)
        #ppm.grantPermissionToPrincipal('uvc.AdHoc', folder.__name__)
        ppm.denyPermissionToPrincipal('uvc.AdHoc', 'uvc.AdHocGroup')
        uvcsite.log('Setting Permission for %s --> %s' % (object, 'uvc.AdHocGroup'))
