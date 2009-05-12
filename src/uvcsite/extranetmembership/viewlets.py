# -*- coding: utf-8 -*-

import grok

from zope import interface
from uvcsite import uvcsiteMF as _

from uvcsite.viewlets.utils import MenuItem
from uvcsite.interfaces import IPersonalMenu


class ExtranetMembership(MenuItem):
    grok.name(_(u'Benutzerverwaltung'))
    grok.context(interface.Interface)
    grok.viewletmanager(IPersonalMenu)
    grok.order(1)

    urlEndings = "enmsindex"
    viewURL = "enmsindex"

