# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from zope import interface, schema

from dolmen.forms.base import set_fields_data
from hurry.workflow.interfaces import IWorkflowInfo
from uvcsite import uvcsiteMF as _
from uvcsite.adhoc.adapter import AdHocUserInfo
from uvcsite.adhoc.interfaces import IAdHocUserInfo, IAdHocFolder
from zeam.form import base


class IWiederaufnahmeArbeit(uvcsite.IContent):

    name = schema.TextLine(
        title=u"Name",
        description=u"Bitte geben Sie den Namen ein",
        )

    datum = schema.Date(
        title = u"Datum",
        description = u"Bitte geben Sie das Datum ein, an dem Sie die Arbeit wieder Aufgenommen haben"
        )


class Wiederaufnahme(uvcsite.Content):
    uvcsite.schema(IWiederaufnahmeArbeit)


class MyAdHocUserInfo(AdHocUserInfo):
    """Adapter"""
    @property
    def isAdHocUser(self):
        if self.context.title.startswith('A'):
            return 1 
        return 0 

    @property
    def addurl(self):
        return "wiederaufnahme"

    @property
    def info(self):
        return "Wiederaufnahme der Arbeit"

    @property
    def defaults(self):
        return {'title': 'Wiederaufnahme'}


class StartseiteMenu(uvcsite.MenuItem):
    grok.layer(uvcsite.adhoc.IAdHocLayer)
    grok.title('Startseite')
    grok.require('uvc.AdHoc')
    grok.viewletmanager(uvcsite.IGlobalMenu)

    action = "index"


class Index(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.layer(uvcsite.adhoc.IAdHocLayer)
    grok.title('Startseite')
    grok.require('uvc.AdHoc')


    title = u"Herzlich Willkommen im Extranet der Novareto"
    description = u"In diesem spezielen Bereich des Extranets können\
            Sie, einmal Dokumente schnell und undbürokratisch an\
            die Berufsgenossenschaft übermittln."

    def update(self):
        self.ahi = IAdHocUserInfo(self.request.principal)
        self.hf = uvcsite.IGetHomeFolderUrl(self.request)

    @property
    def addurl(self):
        url = "%sadhoc/%s" % (self.hf.getURL(), self.ahi.addurl)
        return url


class WiederaufnahmeAddForm(uvcsite.AddForm):
    grok.context(IAdHocFolder)
    grok.name('wiederaufnahme')
    grok.require('uvc.AdHoc')
    ignoreContent = False

    label = description = u"Wiederaufnahme der Arbeit"

    fields = uvcsite.Fields(IWiederaufnahmeArbeit)

    @property
    def defaults(self):
        return dict(title=u"Wiederaufnahme")

    def getContentData(self):
        return base.DictDataManager(self.defaults)

    def create(self, data):
        content = Wiederaufnahme()
        set_fields_data(self.fields, content, data)
        return content

    def add(self, content):
        self.context[self.request.principal.title] = content

    def nextURL(self):
        self.flash(_('Added Content'))
        IWorkflowInfo(self.context[self.request.principal.title]).fireTransition('publish')
        return self.url(self.context[self.request.principal.title])
