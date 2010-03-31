# -*- coding: utf-8 -*-

from grok.interfaces import IContainer
from uvcsite.content import IUVCApplication, IFolderColumnTable
from uvc.layout.interfaces import *


class IUVCSite(IUVCApplication):
    """Marker Interface for UVC-Site Site
    """


class IMyHomeFolder(IContainer, IFolderColumnTable):
    """Marker Interface for HomeFolder
    """

class IGetHomeFolderUrl(Interface):
    """Marker Interface for getting HomeFolderUrls
    """
