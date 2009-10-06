# -*- coding: utf-8 -*-

import grok
import megrok.layout

from uvcsite import uvcsiteMF as _
from uvcsite import ApplicationAwareView
from uvcsite.interfaces import IUVCSite
from uvcsite.auth.handler import setup_pau
from zope.app.security.interfaces import IAuthentication
from uvcsite.homefolder.homefolder import PortalMembership
from zope.app.authentication import PluggableAuthentication
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.publisher.interfaces import INotFound
from zope.publisher.interfaces import INotFound
from zope.interface.common.interfaces import IException
from zope.exceptions.interfaces import IUserError


class Uvcsite(grok.Application, grok.Container):
    """ Application Object for uvc.site"""
    grok.implements(IUVCSite)

    grok.local_utility(PortalMembership,
                       provides=IHomeFolderManager)

    grok.local_utility(PluggableAuthentication,
                       IAuthentication,
                       setup=setup_pau)


class PersonalPanelView(megrok.layout.Page, ApplicationAwareView):
    """ Page for Personal Properties """
    title = _(u"Persönliche Einstellungen")
    description = _(u"Hier können Sie Einstellungen zu"
                     " Ihrem Benutzerprofil vornehmen.")
    grok.require('zope.View')


class NotFound(megrok.layout.Page, ApplicationAwareView):
    grok.context(INotFound)
    grok.name('index.html')

#class SystemError(megrok.layout.Page, ApplicationAwareView):
#      grok.context(IException)
#      grok.name('index.html')

#class UserError(megrok.layout.Page, ApplicationAwareView):
#      grok.context(IUserError)
#      grok.name('index.html')
