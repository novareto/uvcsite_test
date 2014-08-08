# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import uvclight
from GenericCache.GenericCache import GenericCache, default_marshaller
from GenericCache.GenericCache import cached
from grokcore.component import subscribe
from uvc.homefolder.interfaces import IHomefolder
from uvclight.publishing import IModelFoundEvent
from uvcsite.content.interfaces import IProductFolder, IContent
from zope.securitypolicy.interfaces import IPrincipalRoleManager, Allow


permission_cache = GenericCache(expiry=3000, maxsize=5000)


def prm_marshaller(func, node, event):
    # We cache the permissions on the username and the resource path.
    userid = event.request.principal.id
    path = event.request.path
    return repr((func.__name__, userid, path))


@cached(permission_cache, marshaller=prm_marshaller)
@subscribe(IHomefolder, IModelFoundEvent)
@subscribe(IProductFolder, IModelFoundEvent)
@subscribe(IContent, IModelFoundEvent)
def managePermissions(obj, event):
    userid = event.request.principal.id
    for item in uvclight.utils.get_lineage(obj):
        prm = IPrincipalRoleManager(item)
        local_roles = set((role for role, access in
                       prm.getRolesForPrincipal(userid) if access is Allow))
        event.request.principal.roles |= local_roles
        if IHomefolder.providedBy(item):
            break
