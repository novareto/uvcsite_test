# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import uvclight
import uvcsite
from uvcsite.interfaces import IMyRoles
from uvcsite.auth.interfaces import IMasterUser
from uvc.homefolder.interfaces import IHomefolder
from zope.securitypolicy.interfaces import IPrincipalRoleMap, Allow
from zope.security.interfaces import IPrincipal


class MyRoles(uvclight.Adapter):
    uvclight.context(IPrincipal)
    uvclight.implements(IMyRoles)

    def __init__(self, principal):
        self.principal = principal
        self.homefolder = IHomefolder(IMasterUser(self.principal))

    def getAllRoles(self):
        hfr = IPrincipalRoleMap(self.homefolder)
        masteruser = False
        ret = []
        for rolesetting in hfr.getRolesForPrincipal(self.principal.id):
            role, setting = rolesetting
            if 'uvc.Editor' == role and setting is Allow:
                masteruser = True
                ret.append('ENMS')
        for name, productfolder in self.homefolder.items():
            if masteruser:
                ret.append(name)
            else:
                prm = IPrincipalRoleMap(productfolder)
                for rolesetting in prm.getRolesForPrincipal(self.principal.id):
                    role, setting = rolesetting
                    if 'uvc.Editor' == role and setting is Allow:
                        ret.append(name)
        return ret
