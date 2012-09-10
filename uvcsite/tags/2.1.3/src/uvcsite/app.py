# -*- coding: utf-8 -*-
import grok
import uvcsite
import zope.component


from dolmen.app.site import IDolmen
from dolmen.app.layout import errors
from zeam.form.ztk.widgets.date import DateWidgetExtractor, DateFieldWidget

from uvcsite.auth.handler import UVCAuthenticator
from uvcsite.homefolder.homefolder import PortalMembership

from zope.interface import Interface
from zope.i18n.format import DateTimeParseError
from zope.component.interfaces import IComponents
from zope.pluggableauth import PluggableAuthentication
from zope.interface.common.interfaces import IException
from grokcore.registries import create_components_registry
from zope.authentication.interfaces import IAuthentication
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.pluggableauth.interfaces import IAuthenticatorPlugin

from zope.i18n.interfaces import IUserPreferredLanguages
from zope.publisher.interfaces.http import IHTTPRequest
from zeam.form.ztk.widgets.choice import RadioFieldWidget
from zeam.form.ztk.widgets.collection import MultiChoiceFieldWidget


grok.templatedir('templates')


def setup_pau(PAU):
    PAU.authenticatorPlugins = ('principals', )
    PAU.credentialsPlugins = ("cookies",
        "Zope Realm Basic-Auth", "No Challenge if Authenticated")


class Icons(grok.DirectoryResource):
    """Directory Resource for Icons like pdf.png
    """
    grok.name('uvc-icons')
    grok.path('icons')



uvcsiteRegistry = create_components_registry(
    name="uvcsiteRegistry",
    bases = (zope.component.globalSiteManager, ),
    #bases = (),
    )


grok.global_utility(uvcsiteRegistry, name="uvcsiteRegistry", provides=IComponents, direct=True)


class Uvcsite(grok.Application, grok.Container):
    """Application Object for uvc.site
    """
    grok.implements(uvcsite.IUVCSite, IDolmen)

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
            uvcsiteRegistry.__bases__ = tuple([x for x in uvcsiteRegistry.__bases__ if x.__hash__() != zope.component.globalSiteManager.__hash__()])
            current.__bases__ += (uvcsiteRegistry,)
        return current


class NotFound(errors.NotFound):
    """Not Found Error View
    """
    pass


class SystemError(uvcsite.Page):
    """Custom System Error for UVCSITE
    """
    grok.context(IException)
    grok.name('index.html')
    grok.require('zope.Public')


class CustomDateFieldWidget(DateFieldWidget):
    """ Extractor for German Date Notation
    """

    def valueToUnicode(self, value):
        locale = self.request.locale
        formatter = locale.dates.getFormatter(self.valueType, 'medium')
        return formatter.format(value)


class CustomDateWidgetExtractor(DateWidgetExtractor):
    """ Extractor for German Date Notation
    """

    def extract(self):
        value, error = super(DateWidgetExtractor, self).extract()
        if value is not uvcsite.NO_VALUE:
            locale = self.request.locale
            formatter = locale.dates.getFormatter(self.valueType, 'medium')
            try:
                value = formatter.parse(value)
            except (ValueError, DateTimeParseError), error:
                return None, u"Bitte überprüfen Sie das Datumsformat. (tt.mm.jjjj)"
        return value, error


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
