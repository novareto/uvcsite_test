# -*- coding: utf-8 -*-

import grok
import megrok.pagelet

from uvcsite import uvcsiteMF as _
from zope.component import getUtility
from uvcsite.interfaces import IUVCSite
from uvcsite.auth.handler import setup_pau 
from uvcsite.helpsystem.folder import HelpFolder
from zope.app.security.interfaces import IAuthentication
from uvcsite.homefolder.homefolder import PortalMembership
from zope.app.authentication import PluggableAuthentication
from zope.app.homefolder.interfaces import IHomeFolderManager


class Uvcsite(grok.Application, grok.Container):
    """ Application Object for uvc.site"""
    grok.implements(IUVCSite)

    grok.local_utility(PortalMembership,
                       provides=IHomeFolderManager,
                       public=True,
                       name_in_container="members")

    grok.local_utility(PluggableAuthentication, 
                       IAuthentication,
                       setup=setup_pau)

    def traverse(self, name):
        """ Custom Travers Method For the HomeFolders """
        if name == "members":
            utility = getUtility(IHomeFolderManager)
            return utility.homeFolderBase

    def __init__(self):
        super(Uvcsite, self).__init__()
        self['hilfe'] = HelpFolder()


class Index(megrok.pagelet.Pagelet):
    """ Index Site for UVC """
    grok.require('uvc.View')


class Infos(megrok.pagelet.Pagelet):
    """ Info Page for UVC """
    grok.require('uvc.View')


class PersonalPanelView(megrok.pagelet.Pagelet):
    """ Page for Personal Properties """
    grok.require('uvc.View')
    title = _(u"Persönliche Einstellungen")
    description = _(u"Hier können Sie Einstellungen zu" 
                     " Ihrem Benutzerprofil vornehmen.")


class RestLayer(grok.IRESTLayer):
    """ Layer for Rest Access"""
    grok.restskin('api')
