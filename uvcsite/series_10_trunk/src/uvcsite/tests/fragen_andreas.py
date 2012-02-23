# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from uvc import layout
from zope import interface
from megrok import navigation

class AuskunftEntry(grok.View):
    """ Ein Eintrag im Globalen Menu ohne Dropdown
        Achtung in der Zeile layout.menus.category
        dropdown=False
    """
    grok.name('Auskunft')
    grok.title('Auskunft')
    grok.context(interface.Interface)
    navigation.sitemenuitem(uvcsite.IGlobalMenu)
    grok.order(20000)

    def render(self):
        return '<a href="www.google.de"> Google </a>'


class IAuskunft(interface.Interface):
    """ Marker Interface für Auskunft"""


class Auskunft(uvcsite.Page):
    grok.implements(IAuskunft)
    grok.context(uvcsite.IUVCSite)

    def render(self):
        return "<h2> Ich bin eine Auskunftsseite </h2>"
