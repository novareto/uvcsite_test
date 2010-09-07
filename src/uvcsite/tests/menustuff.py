# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

class Kontakt(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(uvcsite.IFooter, order=10)
    grok.require('zope.Public')

    def render(self):
        return "<h1> KONTAKT </h1>"


class Impressum(uvcsite.Page):
    grok.title('Impressum')
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(uvcsite.IFooter)
    grok.require('zope.View')

    def render(self):
        return "IMPRESSUM"


class HelpIndex(uvcsite.Page):
    grok.context(uvcsite.IMyHomeFolder)
    uvcsite.sectionmenu(uvcsite.IGlobalMenu, order=9)

    def render(self):
        return "<h1> HelpINdex </h1>"

class Auskunftsdienste(uvcsite.Category):
    grok.title('Auskunftsdienste')
    uvcsite.topmenu(uvcsite.IGlobalMenu, order=1)


class Unfallbelastung(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.title(u'Unfallbelastung')
    uvcsite.menu(Auskunftsdienste, order=1)

    def render(self):
        return "<h1> Unfallbelastung </h1>"



class DownloadAsPdf(grok.Viewlet):
    grok.title(" ")
    grok.context(uvcsite.IUVCSite)
    grok.view(Kontakt)
    uvcsite.menu(uvcsite.IDocumentActions, order=0, icon="/@@/uvc-icons/icon_pdf.gif")
    group = ""

    

    def render(self):
        return "I could be a PDF"
