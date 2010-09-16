# -*- coding: utf-8 -*-
import grok
import uvcsite

from uvcsite import menu
from uvcsite import uvcsiteMF as _
from dolmen.app.site import IDolmen
from dolmen.app.layout import errors
from uvcsite.auth.handler import setup_pau
from zope.pluggableauth import PluggableAuthentication
from uvcsite.homefolder.homefolder import PortalMembership
from zope.authentication.interfaces import IAuthentication
from zope.app.homefolder.interfaces import IHomeFolderManager

from zeam.form.ztk.widgets.date import DateWidgetExtractor
from zope.i18n.format import DateTimeParseError


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

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       setup=setup_pau)


class PersonalPanelView(uvcsite.Page):
    """Page for Personal Properties
    """
    grok.order(35)

    grok.title(u"Meine Einstellungen")
    title = _(u"Meine Einstellungen")
    description = _(u"Hier werden Einstellungen zu"
                     " Ihrem Benutzerprofil vorgenommen.")

    menu(uvcsite.IPersonalPreferences)


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
