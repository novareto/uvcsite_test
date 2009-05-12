# -*- coding: utf-8 -*-

from zope.interface import Interface


class IUVCSite(Interface):
    """ Markter Interface for UVC-Site Site """

class IContentType(Interface):
    """ Marker Interface for UVC-Site Content Types """


class IHomeFolder(Interface):
    """ Markter Interface for HomeFolder """

# PrincipalAdapters

class ICompanyInfo(Interface):
    """ A Utlity for getting basic 
        data from Companys such as
        address, account information ...
    """

    def getAdresse(mnr):
        """ Return a dict with Adresse """

    def getVeranlagung(mnr):
        """ Return a resultset with veranlagungen"""


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


