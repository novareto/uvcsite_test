# -*- coding: utf-8 -*-

from zope.interface import Interface


class IUVCSite(Interface):
    """ Markter Interface for UVC-Site Site """

class IContentType(Interface):
    """ Marker Interface for UVC-Site Content Types """

class IContainer(Interface):
    """ Marker Interface for UVC-Container """

class IHomeFolder(IContainer):
    """ Markter Interface for HomeFolder """


# ContentProviders

class IHeaders(Interface):
    """ Marker For Headers"""

class IToolbar(Interface):
    """ Marker for Toolbar"""

class IGlobalMenu(Interface):
    """ Marker for GlobalMenu"""

class ISidebar(Interface):
    """ Marker for Sitebar"""

class IFooter(Interface):
    """ Marker for Footer"""

class ILogo(Interface):
    """ Marker for Logo"""

class IPersonalMenu(Interface):
    """ Marker for PersonalMenu """

class IStatusMessage(Interface):                                                
    """ Marker for StatusMessage """

