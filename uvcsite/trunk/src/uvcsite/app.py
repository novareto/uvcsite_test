# -*- coding: utf-8 -*-
import grok
import uvcsite


from dolmen.app.site import IDolmen
from dolmen.app.layout import errors
from zeam.form.ztk.widgets.date import DateWidgetExtractor

from uvcsite import menu
from uvcsite import uvcsiteMF as _
from uvcsite.auth.handler import UVCAuthenticator
from uvcsite.homefolder.homefolder import PortalMembership

from zope.i18n.format import DateTimeParseError
from zope.pluggableauth import PluggableAuthentication
from zope.authentication.interfaces import IAuthentication
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.pluggableauth.interfaces import IAuthenticatorPlugin


def setup_pau_dolmen(PAU):
    PAU.authenticatorPlugins = ('principals', )
    PAU.credentialsPlugins = ("cookies", "No Challenge if Authenticated")


class Icons(grok.DirectoryResource):
    """Directory Resource for Icons like pdf.png
    """
    grok.name('uvc-icons')
    grok.path('icons')



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
                       setup=setup_pau_dolmen)


class PersonalPanelView(uvcsite.Page):
    """Page for Personal Properties
    """
    grok.order(35)

    grok.title(u"Meine Einstellungen")
    title = _(u"Meine Einstellungen")
    description = _(u"Hier werden Einstellungen zu"
                     " Ihrem Benutzerprofil vorgenommen.")

    menu(uvcsite.IPersonalPreferences, order=40)


class NotFound(errors.NotFound):
    """Not Found Error View
    """
    pass


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
                return None, str(error)
        return value, error
