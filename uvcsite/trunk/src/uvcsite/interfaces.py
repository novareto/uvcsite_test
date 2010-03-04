# -*- coding: utf-8 -*-

from grok.interfaces import IContainer
from uvcsite.content import IUVCApplication, IFolderColumnTable
from uvc.layout.interfaces import *


class IUVCSite(IUVCApplication):
    """Markter Interface for UVC-Site Site
    """


class IMyHomeFolder(IContainer, IFolderColumnTable):
    """Markter Interface for HomeFolder
    """
