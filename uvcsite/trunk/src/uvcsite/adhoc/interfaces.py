# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


from zope.interface import Interface
from uvc.layout.layout import IUVCLayer


class IAdHocPrincipal(Interface):
    """ Marker Interface for AdHocPrincipals
    """

class IAdHocLayer(IUVCLayer):
    """ Layer for AdHoc
    """


class IAdHocUserInfo(Interface):
    """ 
    """

    def isAdHocUser():
        """ Return True if the is is a AdHocUser
        """

class IAdHocFolder(Interface):
    """ Marker Interface for AdHocFolder's
    """
