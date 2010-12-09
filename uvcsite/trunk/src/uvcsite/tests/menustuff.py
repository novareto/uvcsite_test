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


class Auskunftsdienste(uvcsite.Category):
    grok.title('Auskunftsdienste')
    uvcsite.topmenu(uvcsite.IGlobalMenu, order=1)


class Unfallbelastung(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.title(u'Unfallbelastung')
    uvcsite.menu(Auskunftsdienste, order=1)

    def render(self):
        return "<h1> Unfallbelastung </h1>"




import tempfile 
class DownloadAsPdf(grok.View):
    grok.title("PDF")
    grok.name('pdf')
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(uvcsite.IDocumentActions, order=0, icon="/@@/uvc-icons/icon_pdf.gif")
    grok.require('zope.Public')
    group = ""


    def render(self):
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-disposition', 'attachment; filename=klaus.txt')
        tmp = tempfile.TemporaryFile()
        tmp.write('klaus')
        tmp.seek(0)
        return tmp.read()

