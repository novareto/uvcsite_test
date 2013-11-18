# -*- coding: utf-8 -*-

import grok
import uvcsite
import zope.component

from uvc.homefolder import Homefolders, IHomefolders
from uvcsite.auth.handler import UVCAuthenticator
from grokcore.registries import create_components_registry
from zope.authentication.interfaces import IAuthentication
from zope.component.interfaces import IComponents
from zope.interface import implementer
from zope.interface.registry import Components
from zope.pluggableauth import PluggableAuthentication
from zope.pluggableauth.interfaces import IAuthenticatorPlugin


grok.templatedir('templates')


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
    grok.local_utility(Homefolders,
                       name_in_container=u"homefolders",
                       public=True,
                       provides=IHomefolders)

    grok.local_utility(UVCAuthenticator,
                       name=u"principals",
                       provides=IAuthenticatorPlugin)

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       public=True,
                       setup=setup_pau)

    def getSiteManager(self):
        current = super(Uvcsite, self).getSiteManager()
        if uvcsiteRegistry not in current.__bases__:
            return Components(bases=(uvcsiteRegistry, current))
        return current


class HAProxyCheck(grok.View):
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    def render(self):
        return "OK"
