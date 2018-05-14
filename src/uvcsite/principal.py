# -*- coding: utf-8 -*-

from zope.pluggableauth import factories
from zope.app.homefolder.interfaces import IHomeFolder
from uvcsite import IGetHomeFolderUrl
from uvcsite.utils import shorties


class Principal(factories.Principal):

    def __repr__(self):
        return "UVCSite_Principal('%s')" % self.id

    @property
    def homefolder(self):
        return IHomeFolder(self).homeFolder

    @property
    def homefolder_url(self):
        request = shorties.getRequest()
        return IGetHomeFolderUrl(request, None)
    
    def getCoUsers(self):
        return None

    def getObjects(self):
        return None
