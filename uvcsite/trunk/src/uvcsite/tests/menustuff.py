# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 


import grok
import uvcsite


class KontaktMenu(uvcsite.MenuItem):
    grok.viewletmanager(uvcsite.IFooter)
    grok.title('Kontakt')
    grok.require('zope.Public')

    action = 'kontakt'


class Kontakt(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    def render(self):
        return "<h1> KONTAKT </h1>"


class MenuImpressum(uvcsite.MenuItem):
    grok.viewletmanager(uvcsite.IFooter)
    grok.require('zope.View')
    grok.title('Impressum')

    action = "impressum"


class Impressum(uvcsite.Page):
    grok.title('Impressum')
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.View')

    def render(self):
        return "IMPRESSUM"

