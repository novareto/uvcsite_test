# -*- coding: utf-8 -*-

import grok

from zope import interface
from uvcsite import uvcsiteMF as _

from uvcsite.viewlets.utils import MenuItem
from uvcsite.interfaces import IPersonalMenu
from zope.app.homefolder.interfaces import IHomeFolder


class ExtranetMembership(MenuItem):
    grok.name(_(u'Benutzerverwaltung'))
    grok.context(interface.Interface)
    grok.viewletmanager(IPersonalMenu)
    grok.order(1)

    urlEndings = "enmsindex"
    @property
    def url(self):
        hF = IHomeFolder(self.request.principal).homeFolder
        return self.view.url(hF, 'enmsindex')

