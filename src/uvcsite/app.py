# -*- coding: utf-8 -*-
import grok

from dolmen.app.layout import models, errors
from dolmen.app.site import IDolmen
from dolmen.menu import menuentry
from uvcsite.auth.handler import setup_pau
from uvcsite import uvcsiteMF as _
from uvcsite.homefolder.homefolder import PortalMembership
from uvcsite.interfaces import IPersonalPreferences
from uvcsite.interfaces import IUVCSite
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.authentication.interfaces import IAuthentication
from zope.pluggableauth import PluggableAuthentication
from zope.interface import Interface
from z3c.form.converter import DateDataConverter
from zope.schema.interfaces import IDate
from z3c.form.interfaces import IWidget, IDataConverter
from megrok.layout import Page
from megrok.icon import IconRegistry

class Icons(IconRegistry):
    grok.name('icons')
    grok.path('/Users/cklinger/community/uvcsite/src/uvcsite/icons')


class Uvcsite(grok.Application, grok.Container):
    """Application Object for uvc.site
    """
    grok.implements(IUVCSite, IDolmen)

    grok.local_utility(PortalMembership,
                       provides=IHomeFolderManager)

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       setup=setup_pau)


@menuentry(IPersonalPreferences, context=Interface)
class PersonalPanelView(Page):
    """Page for Personal Properties
    """
    grok.order(35)
    
    grok.title(u"Meine Einstellungen")
    title = _(u"Meine Einstellungen")
    description = _(u"Hier werden Einstellungen zu"
                     " Ihrem Benutzerprofil vorgenommen.")


class NotFound(errors.NotFound):
    pass

class CustomCalendarDataConverter(DateDataConverter, grok.MultiAdapter):
    """A special calendar data converter for Dates"""
    grok.adapts(IDate, IWidget)
    grok.implements(IDataConverter)
    length = 'medium'


class HelpPage(Page):
    grok.baseclass()

    def namespace(self):
        return {'settings_overrides': {'input_encoding': 'utf-8',
                                       'output_encoding': 'utf-8',
                                       }}
