# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from megrok.z3cform import base as z3cform
from megrok.z3cform.tabular import DeleteFormTablePage
from uvcsite import uvcsiteMF as _
from uvcsite.content import IContent, IProductFolder
from z3c.form import form
from uvcsite.interfaces import IFolderListingTable
from zope.component import getMultiAdapter
from uvcsite import IGetHomeFolderUrl

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


class Add(z3cform.PageAddForm):
    grok.context(IProductFolder)
    grok.require('uvc.AddContent')

    @property
    def fields(self):
        fields = z3cform.meta.get_auto_fields(self.context.getContentType())
        return z3cform.Fields(fields)

    def create(self, data):
        content = self.context.getContentType()()
        form.applyChanges(self, content, data)
        return content

    def add(self, content):
        self.context.add(content)

    def nextURL(self):
        self.flash(_('Added Content'))
        return self.url(self.context)


class Edit(z3cform.PageEditForm):
    grok.context(IContent)
    grok.require('uvc.EditContent')

    @property
    def fields(self):
        return z3cform.Fields(*self.context.schema)


class Display(z3cform.PageDisplayForm):
    grok.context(IContent)
    grok.name('index')
    grok.require('uvc.ViewContent')

    @property
    def fields(self):
        return z3cform.Fields(*self.context.schema)
