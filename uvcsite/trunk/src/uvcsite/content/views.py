# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
from dolmen.forms.base import Fields, set_fields_data, apply_data_event

from megrok.z3cform import base as z3cform
from megrok.z3cform.tabular import DeleteFormTablePage
from uvcsite import uvcsiteMF as _
from uvcsite.content import IContent, IProductFolder
from z3c.form import form
from uvcsite.interfaces import IFolderListingTable
from zope.component import getMultiAdapter
from uvcsite import IGetHomeFolderUrl
from dolmen.content import schema
from zeam.form import base

class Index(DeleteFormTablePage):
    grok.title('Mein Ordner')
    grok.name('index')
    grok.implements(IFolderListingTable) 
    grok.context(IProductFolder)

    cssClasses = {'table': 'myTable tablesorter'}
    cssClassEven = u'even'
    cssClassOdd = u'odd'

    def executeDelete(self, item):
        self.flash(_(u'Ihre Dokumente wurden entfernt'))
        del item.__parent__[item.__name__]

    def getAddLinkUrl(self):
        adapter = getMultiAdapter((self.request.principal, self.request), IGetHomeFolderUrl)
        return adapter.getAddURL(self.context.getContentType())


class Add(uvcsite.AddForm):
    grok.context(IProductFolder)
    grok.require('uvc.AddContent')

    @property
    def fields(self):
        content_object = self.context.getContentType()
        schemas = schema.bind().get(content_object)
        return Fields(*schemas)

    def create(self, data):
        content = self.context.getContentType()()
        set_fields_data(self.fields, content, data)
        return content

    def add(self, content):
        self.context.add(content)

    def nextURL(self):
        self.flash(_('Added Content'))
        return self.url(self.context)


class Edit(uvcsite.Form):
    grok.context(IContent)
    grok.require('uvc.EditContent')
    ignoreContent = False

    @property
    def fields(self):
        content_object = self.context
        schemas = schema.bind().get(content_object)
        return Fields(*schemas)

    @base.action(u'Speichern')
    def handle_apply(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type="error")
            return
        changes = apply_data_event(self.fields, self.context, data)
        if changes:
            self.flash(u'Ihre Daten wurden erfolgreich gendert', type="info")
            return
        else:
            self.flash('Kein Änderung', type="info")


class Display(uvcsite.Form):
    grok.context(IContent)
    grok.name('index')
    grok.require('uvc.ViewContent')

    mode = base.DISPLAY
    ignoreContent = False

    @property
    def fields(self):
        content_object = self.context
        schemas = schema.bind().get(content_object)
        return Fields(*schemas)
