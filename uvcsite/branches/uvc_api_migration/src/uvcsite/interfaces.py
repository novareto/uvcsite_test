# -*- coding: utf-8 -*-

from cromlech.container.interfaces import IContainer
from uvcsite.content import IUVCApplication, IFolderColumnTable
from zope.interface import Interface
from uvclight import IApplication as IUVCSite


class IMyHomeFolder(IContainer, IFolderColumnTable):
    """Marker Interface for HomeFolder
    """


class IGetHomeFolderUrl(Interface):
    """Marker Interface for getting HomeFolderUrls
    """


class IFolderListingTable(Interface):
    """Marker Interface for tables with a listing interface
       for contenttypes
    """


class IMyRoles(Interface):
    """Return all allowed Roles in various forms
    """
