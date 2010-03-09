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


class Uvcsite(grok.Application, grok.Container):
    """Application Object for uvc.site
    """
    grok.implements(IUVCSite, IDolmen)

    grok.local_utility(PortalMembership,
                       provides=IHomeFolderManager)

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       setup=setup_pau)


@menuentry(IPersonalPreferences)
class PersonalPanelView(models.Page):
    """Page for Personal Properties
    """
    grok.order(35)
    
    grok.title(u"Meine Einstellungen")
    title = _(u"Meine Einstellungen")
    description = _(u"Hier werden Einstellungen zu"
                     " Ihrem Benutzerprofil vorgenommen.")


class NotFound(errors.NotFound):
    pass
