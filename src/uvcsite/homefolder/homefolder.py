# -*- coding: utf-8 -*-

import grok

from uvcsite.interfaces import IMyHomeFolder
from uvcsite.auth.interfaces import IMasterUser

from zope.app.homefolder.homefolder import HomeFolderManager
from zope.app.homefolder.interfaces import IHomeFolderManager
import zope.app.homefolder.homefolder
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.dottedname.resolve import resolve
from zope.security.interfaces import IPrincipal


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


@grok.subscribe(IHomeFolderManager, grok.IObjectAddedEvent)
def add_members_folder(object, event):
    object.__parent__.__parent__['members'] = Members()
