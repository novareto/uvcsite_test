# -*- coding: utf-8 -*-

import grok
import uvcsite
import zope.component
import grokcore.component

from uvc.homefolder import Homefolders, IHomefolders
from uvcsite.auth.handler import UVCAuthenticator
from grokcore.registries import create_components_registry
from zope.authentication.interfaces import IAuthentication
from zope.component.interfaces import IComponents
from zope.interface import implementer
from zope.interface.registry import Components
from zope.pluggableauth import PluggableAuthentication
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.site.site import LocalSiteManager as BaseLocalSiteManager
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from grokcore.site.components import BaseSite
from zope.site.site import SiteManagerContainer
from grokcore.site import IApplication


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


class LocalSiteManager(BaseLocalSiteManager):

    __bases__ = property(
        lambda self: (uvcsiteRegistry,) + self.__dict__.get('__bases__', tuple()),
        lambda self, bases: self._setBases(bases),
    )


@implementer(uvcsite.IUVCSite, IApplication)
class Uvcsite(BaseSite, SiteManagerContainer, grok.Container):
    """Application Object for uvc.site
    """

    _managerClass = LocalSiteManager

    grok.local_utility(Homefolders,
                       name_in_container=u"members",
                       public=True,
                       provides=IHomefolders)

    grok.local_utility(UVCAuthenticator,
                       name=u"principals",
                       provides=IAuthenticatorPlugin)

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       public=True,
                       setup=setup_pau)


@grokcore.component.subscribe(uvcsite.IUVCSite, IObjectAddedEvent)
def addSiteHandler(site, event):
    manager = site._managerClass
    sitemanager = manager(site, default_folder=False)
    site.setSiteManager(sitemanager)


class HAProxyCheck(grok.View):
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    def render(self):
        return "OK"

    
class Debug(grok.View):
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    def render(self):
        import pdb
        pdb.set_trace()


class Migration(grok.View):
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    def render(self):
        try:
            # migration of member area
            hf = self.context['members']
            if hasattr(hf, '_data') is False:
                hf._data = hf._SampleContainer__data
                del hf._SampleContainer__data
                print "migrated Homefolders structure"

            for user in self.context['members'].values():
                if hasattr(user, '_data') is False:
                    user._data = user._SampleContainer__data
                    del user._SampleContainer__data
                    print "migrated user %s" % user.__name__
            
            # migration of the sm
            if self.context._sm.__class__ != LocalSiteManager:
                newsm = LocalSiteManager(self.context, default_folder=False)
                newsm.addSub(self.context._sm)
                self.context._sm = newsm
                print "migrated sm"
        
            # Add membership to sm
            if self.context._sm.queryUtility(IHomefolders) is None:
                members = self.context['members']
                self.context._sm.registerUtility(members, IHomefolders)
                print "Added IHomefolders"

        except Exception, e:
            import pdb
            pdb.set_trace()
