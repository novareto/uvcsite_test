# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import uvclight
from grokcore.security import Role, Permission, permissions
from zope.securitypolicy.interfaces import IRolePermissionManager
from uvcsite.workflow.basic_workflow import PUBLISHED
from hurry.workflow.interfaces import IWorkflowTransitionEvent
from grokcore.component import subscribe


class User(Role):
    uvclight.name('uvc.User')
    permissions('zope.View')


class Editor(Role):
    uvclight.name('uvc.Editor')
    permissions('uvc.AddContent', 'uvc.ViewContent', 'uvc.EditContent')


class View(Permission):
    uvclight.name('uvc.ViewContent')


class Add(Permission):
    uvclight.name('uvc.AddContent')


class Edit(Permission):
    uvclight.name('uvc.EditContent')


@subscribe(IWorkflowTransitionEvent)
def remove_edit_permission(event):
    if event.destination != PUBLISHED:
        return
    IRolePermissionManager(event.object).denyPermissionToRole(
           'uvc.EditContent', 'uvc.Editor')
