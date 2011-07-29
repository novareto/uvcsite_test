# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


import grok
import uvcsite

from dolmen.security.policies.principalrole import ExtraRoleMap

from zope.securitypolicy.interfaces import Allow
from zope.securitypolicy.securitymap import SecurityMap
from zope.securitypolicy.interfaces import (
     IPrincipalRoleManager, IPrincipalRoleMap, IRolePermissionMap, IPrincipalPermissionManager)


class AdHoc(grok.Permission):
    grok.name('uvc.AdHoc')


from zope.securitypolicy.principalpermission import principalPermissionManager as prinperG
prinperG.grantPermissionToPrincipal('uvc.AdHoc', 'uvc.AdHocGroup', False)




#class AdHocPrincipalRoleManager(ExtraRoleMap):
#    grok.implements(IPrincipalRoleManager, IPrincipalRoleMap, IPrincipalPermissionManager)
#
#    def _compute_extra_data(self):
#        extra_map = SecurityMap()
#        extra_map.addCell('uvc.AdHoc', 'uvc.AdHocGroup', Allow)
#        return extra_map
#
#from grokcore.component import global_adapter
##global_adapter(AdHocPrincipalRoleManager, (uvcsite.IUVCSite,), IPrincipalRoleMap)
#global_adapter(AdHocPrincipalRoleManager, (uvcsite.IUVCSite,), IPrincipalRoleManager)
#global_adapter(AdHocPrincipalRoleManager, (uvcsite.IUVCSite,), IPrincipalPermissionManager)
