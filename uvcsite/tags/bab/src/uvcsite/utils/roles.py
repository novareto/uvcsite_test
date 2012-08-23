# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope.security.interfaces import IPrincipal
from uvcsite.auth.interfaces import IMasterUser
from zope.app.homefolder.interfaces import IHomeFolder
from zope.securitypolicy.interfaces import IPrincipalRoleMap, Allow


class MyRoles(grok.Adapter):
    grok.context(IPrincipal)
    grok.implements(uvcsite.IMyRoles)

    def __init__(self, principal):
        self.principal = principal
        self.homefolder = IHomeFolder(IMasterUser(self.principal)).homeFolder

    def getAllRoles(self):
        hfr = IPrincipalRoleMap(self.homefolder)
        masteruser = False
        ret = []
        for rolesetting in hfr.getRolesForPrincipal(self.principal.id):
            role, setting = rolesetting
            if 'uvc.Editor' == role and setting is Allow:
                masteruser = True
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
