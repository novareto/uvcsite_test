# -*- coding: utf-8 -*-

import grok

from uvcsite import uvcsiteMF as _
from zope.interface import Interface
from uvcsite.interfaces import ISidebar 
from uvcsite.viewlets.utils import MenuItem

from z3c.menu.simple.menu import GlobalMenuItem


class Beispiel(MenuItem):
    """ Image Things"""
    grok.name(_(u'Startseite'))
    grok.context(Interface)
    grok.viewletmanager(ISidebar)

    urlEndings = "index"
    viewURL = "index"


class Informationen(MenuItem):
    """ Image Things"""
    grok.name(_('Allgemeine Informationen'))
    grok.context(Interface)
    grok.viewletmanager(ISidebar)

    urlEndings = "infos"
    viewURL = "infos"

