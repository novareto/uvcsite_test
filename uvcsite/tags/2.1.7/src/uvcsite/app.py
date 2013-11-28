# -*- coding: utf-8 -*-
import grok
import uvcsite

from dolmen.app.site import IDolmen

from uvcsite.auth.handler import UVCAuthenticator
from uvcsite.homefolder.homefolder import PortalMembership


from grokcore.registries import create_components_registry
from zeam.form.base import NO_VALUE
from zeam.form.ztk import customize
from zeam.form.ztk.widgets.choice import RadioFieldWidget
from zeam.form.ztk.widgets.collection import MultiChoiceFieldWidget
from zeam.form.ztk.widgets.date import DateWidgetExtractor
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.authentication.interfaces import IAuthentication
from zope.component.interfaces import IComponents
from zope.i18n.format import DateTimeParseError
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.interface import Interface
from zope.pluggableauth import PluggableAuthentication
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.publisher.interfaces.http import IHTTPRequest
from zope.schema.interfaces import IDate
from grokcore.site import IApplication
from zope.component import globalSiteManager


grok.templatedir('templates')


def setup_pau(PAU):
    PAU.authenticatorPlugins = ('principals', )
    PAU.credentialsPlugins = ("cookies",
                              "Zope Realm Basic-Auth",
                              "No Challenge if Authenticated",)


class Icons(grok.DirectoryResource):
    """Directory Resource for Icons like pdf.png
    """
    grok.name('uvc-icons')
    grok.path('icons')


uvcsiteRegistry = create_components_registry(
    name="uvcsiteRegistry",
)


grok.global_utility(
    uvcsiteRegistry,
    name="uvcsiteRegistry",
    provides=IComponents,
    direct=True)


class Uvcsite(grok.Application, grok.Container):
    """Application Object for uvc.site
    """
    grok.implements(uvcsite.IUVCSite, IDolmen, IApplication)

    grok.local_utility(PortalMembership,
                       provides=IHomeFolderManager)

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
            uvcsiteRegistry.__bases__ = tuple(
                [x for x in uvcsiteRegistry.__bases__
                    if x._hash_() != globalSiteManager._hash_()])
            current.__bases__ = (uvcsiteRegistry,) + current.__bases__
        elif current.__bases__[0] is not uvcsiteRegistry:
            current.__bases__ = (uvcsiteRegistry,) + tuple((
                b for b in current.__bases__ if b != uvcsiteRegistry))
        return current


class NotFound(uvcsite.Page, grok.components.NotFoundView):
    """Not Found Error View
    """
    pass


class SystemError(uvcsite.Page, grok.components.ExceptionView):
    """Custom System Error for UVCSITE
    """

    def __init__(self, context, request):
        super(SystemError, self).__init__(context, request)
        self.context = grok.getSite()
        self.origin_context = context


class UVCDateWidgetExtractor(DateWidgetExtractor):

    def extract(self):
        value, error = super(DateWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            if not len(value):
                return NO_VALUE, None
            formatter = self.component.getFormatter(self.form)
            try:
                value = formatter.parse(value)
            except (ValueError, DateTimeParseError), error:
                return None, u"Bitte überprüfen Sie das Datumsformat."
        return value, error


@customize(origin=IDate)
def customize_size(field):
    field.valueLength = 'medium'


class Favicon(grok.View):
    """ Helper for Favicon.ico Errors Request
    """
    grok.context(Interface)
    grok.name('favicon.ico')
    grok.require('zope.Public')

    def render(self):
        return "BLA"


class GermanBrowserLangugage(grok.Adapter):
    grok.context(IHTTPRequest)
    grok.implements(IUserPreferredLanguages)

    def getPreferredLanguages(self):
        return ['de', 'de-de']


class UvcRadioFieldWidget(RadioFieldWidget):
    """ Simple Override for removing <br> between choices
    """
    pass


class UvcMultiChoiceFieldWidget(MultiChoiceFieldWidget):
    """ Simple Override for removing <br> between choices
    """


class HAProxyCheck(grok.View):
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    def render(self):
        return "OK"
