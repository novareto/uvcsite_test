# -*- coding: utf-8 -*-


from zope.interface import classImplements
from uvc.homefolder.components import Homefolder
from uvcsite.interfaces import IFolderColumnTable


# For the table display
classImplements(Homefolder, IFolderColumnTable)
