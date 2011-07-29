# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


from zope.interface import Interface
from grok.interfaces import IContainer
from uvc.layout.layout import IUVCBaseLayer
from uvcsite.content import IUVCApplication, IFolderColumnTable


class IAdHocPrincipal(Interface):
    """ Marker Interface for AdHocPrincipals
    """


class IAdHocLayer(IUVCBaseLayer):
    """ Layer for AdHoc
    """


class IAdHocUserInfo(Interface):
    """ 
    """

    def isAdHocUser():
        """ Return True if the is is a AdHocUser
        """


class IAdHocFolder(IContainer, IFolderColumnTable):
    """ Marker Interface for AdHocFolder's
    """
