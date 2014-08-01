# -*- coding: utf-8 -*-

## import grok
## import uvcsite

## from uvcsite.content import IProductFolder
## from uvcsite.interfaces import IMyHomeFolder, IGetHomeFolderUrl
## from uvcsite.auth.interfaces import IMasterUser

## from zope.app.homefolder.homefolder import HomeFolderManager
## from zope.app.homefolder.interfaces import IHomeFolderManager
## import zope.app.homefolder.homefolder
## from zope.component import getUtilitiesFor
## from zope.securitypolicy.interfaces import IPrincipalRoleManager
## from zope.dottedname.resolve import resolve
## from zope.security.interfaces import IPrincipal
## from zope.app.security.interfaces import IUnauthenticatedPrincipal
## from zope.app.homefolder.interfaces import IHomeFolder
## from zope.publisher.interfaces.browser import IBrowserRequest

# import zope.securitypolicy.interfaces
# import zope.securitypolicy.principalrole

# class PrincipalRoleManager(
#     zope.securitypolicy.principalrole.AnnotationPrincipalRoleManager,
#     grok.Adapter):

#     grok.context(IMyHomeFolder)

#     def getRolesForPrincipal(self, principal_id):
#         ''' See the interface IPrincipalRoleMap '''
#         roles = super(PrincipalRoleManager, self).getRolesForPrincipal(principal_id)
#         roles.append(('zope.Manager', zope.securitypolicy.interfaces.Allow))
#         return roles
