# -*- coding: utf-8 -*-

import grok
import uvcsite

from uvcsite.content import IProductFolder
from uvcsite.interfaces import IMyHomeFolder, IGetHomeFolderUrl
from uvcsite.auth.interfaces import IMasterUser

from zope.app.homefolder.homefolder import HomeFolderManager
from zope.app.homefolder.interfaces import IHomeFolderManager
import zope.app.homefolder.homefolder
from zope.component import getUtilitiesFor
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.dottedname.resolve import resolve
from zope.security.interfaces import IPrincipal
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zope.app.homefolder.interfaces import IHomeFolder
from zope.traversing.browser.absoluteurl import  absoluteURL
from zope.publisher.interfaces.browser import IBrowserRequest


class HomeFolder(grok.Container):
    grok.implements(IMyHomeFolder)


class Members(grok.Container):
    pass


class PortalMembership(HomeFolderManager):
    """
    """
    grok.implements(IHomeFolderManager)

    autoCreateAssignment = True
    homeFolderRole = [u'uvc.User', u'uvc.Editor', u'uvc.MasterUser']
    containerObject = 'uvcsite.homefolder.homefolder.HomeFolder'

    def assignHomeFolder(self, principalId, folderName=None, create=None):
        """See IHomeFolderManager"""
        # The name of the home folder is folderName, if specified, otherwise
        # it is the principal id
        name = folderName or principalId
        # Make the assignment.
        self.assignments[principalId] = name

        # Create a home folder instance, if the correct flags are set.
        if (create is True) or (create is None and self.createHomeFolder):
            if name not in self.homeFolderBase:
                objectToCreate = resolve(self.containerObject)
                self.homeFolderBase[name] = objectToCreate()
            principal_roles = IPrincipalRoleManager(self.homeFolderBase[name])
            for role in self.homeFolderRole:
                principal_roles.assignRoleToPrincipal(
                    role, principalId)

    @property
    def homeFolderBase(self):
        return grok.getSite()['members']


class HomeFolderForPrincipal(grok.Adapter,
                             zope.app.homefolder.homefolder.HomeFolder):
    grok.context(IPrincipal)

    def __init__(self, principal):
        self.principal = IMasterUser(principal)


class HomeFolderUrl_deprecated(grok.MultiAdapter):
    grok.adapts(IPrincipal, IBrowserRequest)
    grok.implements(IGetHomeFolderUrl)

    def __init__(self, context, request):
        adapter = IGetHomeFolderUrl(request)
        self.getURL = adapter.getURL
        self.getAddURL = adapter.getAddURL


class HomeFolderUrl(grok.Adapter):

    grok.context(IBrowserRequest)
    grok.implements(IGetHomeFolderUrl)

    def __init__(self, request):
        self.request = request

    def getURL(self, type=""):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal).homeFolder
        homeFolder = grok.url(self.request, homeFolder, type)
        return homeFolder

    def getAddURL(self, type):
        productfolders = list(getUtilitiesFor(IProductFolder))
        for name, class_ in productfolders:
            if uvcsite.contenttype.bind().get(class_) is type:
                url = "%s/@@add" % self.getURL(name)
                return url


@grok.subscribe(IHomeFolderManager, grok.IObjectAddedEvent)
def add_members_folder(object, event):
    object.__parent__.__parent__['members'] = Members()


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
