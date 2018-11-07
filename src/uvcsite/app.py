# -*- coding: utf-8 -*-
# Copyright (c) 2007-2013 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
import uvcsite.plugins
import zope.component

from grokcore.registries import create_components_registry
from uvcsite.interfaces import IHomeFolderManager
from zope.authentication.interfaces import IAuthentication
from zope.component import globalSiteManager
from zope.component.interfaces import IComponents
from zope.interface import implementer
from zope.pluggableauth import PluggableAuthentication
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from uvcsite.auth.handler import UVCAuthenticator
from uvcsite.homefolder.homefolder import PortalMembership


def setup_pau(PAU):
    PAU.authenticatorPlugins = ('principals', )
    PAU.credentialsPlugins = ("cookies",
                              "Zope Realm Basic-Auth",
                              "No Challenge if Authenticated",)


uvcsiteRegistry = create_components_registry(
    name="uvcsiteRegistry",
    bases=(zope.component.globalSiteManager, ),
)


grok.global_utility(
    uvcsiteRegistry,
    name="uvcsiteRegistry",
    provides=IComponents,
    direct=True)


@implementer(uvcsite.IUVCSite) 
class Uvcsite(grok.Application, grok.Container):
    """Application Object for uvc.site
    """
    grok.traversable('plugins')
    
    grok.local_utility(PortalMembership,
                       provides=IHomeFolderManager)

    grok.local_utility(UVCAuthenticator,
                       name=u"principals",
                       provides=IAuthenticatorPlugin)

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       public=True,
                       setup=setup_pau)

    @property
    def plugins(self):
        return uvcsite.plugins.PluginsPanel('plugins', self)

    def getSiteManager(self):
        current = super(Uvcsite, self).getSiteManager()
        if uvcsiteRegistry not in current.__bases__:
            uvcsiteRegistry.__bases__ = tuple(
                [x for x in uvcsiteRegistry.__bases__
                    if (hasattr(x, '_hash_') and
                        x._hash_() != globalSiteManager._hash_())])
            current.__bases__ = (uvcsiteRegistry,) + current.__bases__
        elif current.__bases__[0] is not uvcsiteRegistry:
            current.__bases__ = (uvcsiteRegistry,) + tuple((
                b for b in current.__bases__ if b != uvcsiteRegistry))
        return current
