# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from uvc import layout
from zope import interface

class AuskunftEntry(uvcsite.Entry):
    """ Ein Eintrag im Globalen Menu ohne Dropdown
        Achtung in der Zeile layout.menus.category
        dropdown=False
    """
    grok.name('Auskunft')
    grok.title('Auskunft')
    grok.context(interface.Interface)
    uvcsite.menu(uvcsite.GlobalMenu)
    layout.menus.category(u'Auskunft', url='auskunft', dropdown=False)
    grok.order(100)

    def render(self):
        return '<a href="www.google.de"> Google </a>'


class IAuskunft(interface.Interface):
    """ Marker Interface für Auskunft"""


class Auskunft(uvcsite.Page):
    grok.implements(IAuskunft)
    grok.context(uvcsite.IUVCSite)

    def render(self):
        return "<h2> Ich bin eine Auskunftsseite </h2>"


@uvcsite.menuentry(uvcsite.IDocumentActions, view=IAuskunft)
class AuskunftPdf(grok.View):
    grok.context(uvcsite.IUVCSite)

    def render(self):
        return "PDF"


#class AuskunftDokumentAction(uvcsite.Entry):
#    grok.context(uvcsite.IUVCSite)
#    grok.view(Auskunft)
#    uvcsite.menu(uvcsite.DocumentActionsMenu)
#
#    def render(self):
##        return "PDF"
