# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

## from zope.interface import Interface
## from uvcsite import uvcsiteMF as _
## from uvc.layout import interfaces
## from uvc.layout.slots import menus
## from uvcsite.content import IContent, IProductFolder
## from uvcsite.interfaces import IFolderListingTable
## from zope.component import getMultiAdapter
## from uvcsite import IGetHomeFolderUrl
## from dolmen.content import schema
## from dolmen import menu
## from dolmen.app.layout.viewlets import ContextualActions
## from zeam.form.base.interfaces import ISimpleForm


import uvclight
import uvcsite
from cromlech.browser import ITemplate
from dolmen.forms import base
from dolmen.forms.base import Fields, set_fields_data, apply_data_event
from uvc.content import IContent
from uvcsite.interfaces import IFolderListingTable
from .interfaces import IProductFolder
from zope.component import getMultiAdapter
from uvc.design.canvas.managers import ITabs
from zope.interface import Interface


class WhatAmI(uvclight.View):

    def render(self):
        from cgi import escape
        from zope.interface import providedBy
        return '<pre>%s</pre>' % '\n'.join(
            [escape(str(iface)) for iface in providedBy(self.context)])


class Display(uvclight.Form):
    uvclight.context(IContent)
    uvclight.name('index')
    uvclight.require('uvc.ViewContent')

    mode = base.DISPLAY
    ignoreContent = False

    @property
    def fields(self):
        content_object = self.context
        schemas = uvclight.schema.bind().get(content_object)
        return Fields(*schemas)
     

class Index(uvclight.TablePage):
    uvclight.title(u'Übersicht')
    uvclight.name('index')
    uvclight.implements(IFolderListingTable)
    uvclight.context(IProductFolder)

    description = u"Hier finden Sie alle Dokumente dazu."

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
        uvclight.TablePage.update(self)

    def executeDelete(self, item):
        self.flash(_(u'Ihre Dokumente wurden entfernt'))
        del item.__parent__[item.__name__]

    def getAddLinkUrl(self):
        adapter = getMultiAdapter(
            (self.request.principal, self.request), IGetHomeFolderUrl)
        return adapter.getAddURL(self.context.getContentType())

    def getAddTitle(self):
        return self.context.getContentName()

    @property
    def values(self):
        #~ FIXME
        return []


class AddMenuViewlet(uvclight.Viewlet):
    uvclight.view(Index)
    uvclight.order(30)
    uvclight.context(IProductFolder)
    uvclight.viewletmanager(ITabs)

    @property
    def template(self):
        return getMultiAdapter((self, self.request), ITemplate)



@uvclight.adapter(AddMenuViewlet, Interface)
@uvclight.implementer(ITemplate)
def add_menu(context, request):
    return uvclight.get_template('addmenu.cpt', __file__)



class Add(uvclight.AddForm):
    uvclight.context(IProductFolder)
    uvclight.require('uvc.AddContent')

    @property
    def label(self):
        return self.context.__class__.__name__

    description = u"Bitte füllen Sie die Eingabeform."

    @property
    def fields(self):
        content_object = self.context.getContentType()
        schemas = uvclight.schema.bind().get(content_object)
        return base.Fields(*schemas)

    def create(self, data):
        content = self.context.getContentType()()
        set_fields_data(self.fields, content, data)
        return content

    def add(self, content):
        self.context.add(content)

    def nextURL(self):
        self.flash(_('Added Content'))
        return self.url(self.context)



    
## uvclight.templatedir('templates')


## class ExtraViewsViewlet(ContextualActions):
##     uvclight.order(20)
##     uvclight.baseclass()
##     uvclight.view(Interface)
##     uvclight.name('extra-views')
##     uvclight.viewletmanager(interfaces.IAboveContent)
##     uvclight.require("zope.Public")

##     #menu_factory = menus.ExtraViews
##     menu_factory = object()

##     def update(self):
##         MenuViewlet.update(self)
##         if not len(self.menu.viewlets) or ISimpleForm.providedBy(self.view):
##             self.actions = None
##         else:
##             self.actions = self.compute_actions(self.menu.viewlets)

##     def compute_actions(self, viewlets):
##         for action in viewlets:
##             selected = action.viewName == self.view.__name__
##             context_url = self.menu.view.url(self.menu.context)
##             url = not selected and "%s/%s" % (context_url, action.viewName) or None
##             yield {
##                 'id': action.__name__,
##                 'url': url,
##                 'title': action.title or action.__name__,
##                 'selected': selected,
##                 'class': (selected and 'selected ' +
##                           self.menu.menu_class or self.menu.menu_class),
##                 }







## class Edit(uvcsite.Form):
##     uvclight.context(IContent)
##     uvclight.require('uvc.EditContent')
##     ignoreContent = False

##     @property
##     def fields(self):
##         content_object = self.context
##         schemas = schema.bind().get(content_object)
##         return Fields(*schemas)

##     @base.action(u'Speichern')
##     def handle_apply(self):
##         data, errors = self.extractData()
##         if errors:
##             self.flash('Es sind Fehler aufgetreten', type="error")
##             return
##         changes = apply_data_event(self.fields, self.context, data)
##         if changes:
##             self.flash(u'Ihre Daten wurden erfolgreich gendert', type="info")
##             return
##         else:
##             self.flash('Kein Änderung', type="info")


