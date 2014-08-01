# -*- coding: utf-8 -*-

## import grok
## import uvcsite
# import zope.securitypolicy.interfaces
# import zope.securitypolicy.principalrole

## from uvcsite.content import IProductFolder
## from zope.component import getUtilitiesFor
## from zope.securitypolicy.interfaces import IPrincipalRoleManager
## from zope.dottedname.resolve import resolve
## from zope.security.interfaces import IPrincipal


# class PrincipalRoleManager(
#     zope.securitypolicy.principalrole.AnnotationPrincipalRoleManager,
#     grok.Adapter):

#     grok.context(IMyHomeFolder)

#     def getRolesForPrincipal(self, principal_id):
#         ''' See the interface IPrincipalRoleMap '''
#         roles = super(PrincipalRoleManager, self).getRolesForPrincipal(principal_id)
#         roles.append(('zope.Manager', zope.securitypolicy.interfaces.Allow))
#         return roles
