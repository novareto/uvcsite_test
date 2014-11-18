# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
from dolmen.forms.base import Fields, set_fields_data, apply_data_event

from zope.interface import Interface
from uvcsite import uvcsiteMF as _
from uvc.layout import interfaces
from uvc.layout.slots import menus
from dolmen.app.layout import MenuViewlet
from uvcsite.content import IContent, IProductFolder
from uvcsite.interfaces import IFolderListingTable
from zope.component import getMultiAdapter
from uvcsite import IGetHomeFolderUrl
from dolmen.content import schema
from dolmen import menu
from zeam.form import base
from uvc.layout import TablePage
from dolmen.app.layout.viewlets import ContextualActions
from zeam.form.base.interfaces import ISimpleForm
from megrok.pagetemplate import PageTemplate
from zope.pagetemplate.interfaces import IPageTemplate


grok.templatedir('templates')


class Index(TablePage):
    grok.title(u'Übersicht')
    grok.name('index')
    grok.implements(IFolderListingTable)
    grok.context(IProductFolder)
    grok.require('uvc.ViewContent')

    description = u"Hier finden Sie alle Dokumente dazu."

    cssClasses = {'table': 'tablesorter table table-striped table-bordered table-condensed'}
    cssClassEven = u'even'
    cssClassOdd = u'odd'

    sortOnId = "table-modified-5"
    sortOn = "table-modified-5"
    #sortOrder = "down"

    @property
    def title(self):
        return self.context.getContentName()

    def update(self):
        items = self.request.form.get('table-checkBox-0-selectedItems')
        if items and self.request.has_key('form.button.delete'):
            if isinstance(items, (str, unicode)):
                items = [items,]
            for key in items:
                if self.context.has_key(key):
                    self.executeDelete(self.context[key])
        TablePage.update(self)

    def executeDelete(self, item):
        self.flash(_(u'Ihre Dokumente wurden entfernt'))
        del item.__parent__[item.__name__]

    def getAddLinkUrl(self):
        adapter = getMultiAdapter(
            (self.request.principal, self.request), IGetHomeFolderUrl)
        return adapter.getAddURL(self.context.getContentType())

    def getAddTitle(self):
        return self.context.getContentName()


class ExtraViewsViewlet(ContextualActions):
    grok.order(20)
    grok.baseclass()
    grok.view(Interface)
    grok.name('extra-views')
    grok.viewletmanager(interfaces.IAboveContent)
    grok.require("zope.Public")

    #menu_factory = menus.ExtraViews
    menu_factory = object()

    def update(self):
        MenuViewlet.update(self)
        if not len(self.menu.viewlets) or ISimpleForm.providedBy(self.view):
            self.actions = None
        else:
            self.actions = self.compute_actions(self.menu.viewlets)

    def compute_actions(self, viewlets):
        for action in viewlets:
            selected = action.viewName == self.view.__name__
            context_url = self.menu.view.url(self.menu.context)
            url = not selected and "%s/%s" % (context_url, action.viewName) or None
            yield {
                'id': action.__name__,
                'url': url,
                'title': action.title or action.__name__,
                'selected': selected,
                'class': (selected and 'selected ' +
                          self.menu.menu_class or self.menu.menu_class),
                }


class AddMenuViewlet(grok.Viewlet):
    grok.view(Index)
    grok.order(30)
    grok.context(IProductFolder)
    grok.viewletmanager(interfaces.ITabs)

    def render(self):
        template = getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class AddMenu(PageTemplate):
    grok.view(AddMenuViewlet)


class Add(uvcsite.AddForm):
    grok.context(IProductFolder)
    grok.require('uvc.AddContent')

    @property
    def label(self):
        return self.context.getContentName()

    description = u"Bitte füllen Sie die Eingabeform."

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


class EditSite(Edit):
    grok.name('edit')
    grok.context(uvcsite.IUVCSite)
    ignoreContent = False
    fields = Fields(uvcsite.IUVCSite)
            
    @base.action(u'Speichern')
    def handle_apply(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type="error")
            return

        self.context.logo = data['logo']
        self.flash(u'Ihre Daten wurden erfolgreich gendert', type="info")
        return


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

