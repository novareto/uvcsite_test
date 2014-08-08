# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de


from grokcore.component import subscribe
from zope.securitypolicy.interfaces import IPrincipalRoleManager, Allow
from uvclight.publishing import IModelFoundEvent
from uvc.homefolder.interfaces import IHomefolder
from uvcsite.content.interfaces import IProductFolder, IContent


@subscribe(IHomefolder, IModelFoundEvent)
@subscribe(IProductFolder, IModelFoundEvent)
@subscribe(IContent, IModelFoundEvent)
def managePermissions(obj, event):
    permissions = []
    while obj is not None:
        print obj
        prm = IPrincipalRoleManager(obj)
        permissions += [r for r, s in prm.getRolesForPrincipal(event.request.principal.id) if s is Allow]
        if IHomefolder.providedBy(obj):
            obj = None
        else:
            obj = obj.__parent__
    event.request.principal.roles += permissions
