# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope.interface import Interface
from uvcsite import uvcsiteMF as _
from megrok.z3ctable import Values
from megrok.z3ctable import TablePage
from zope.traversing.browser import absoluteURL
from uvcsite.interfaces import IMyHomeFolder, IFolderListingTable
from uvc.layout import interfaces
from uvcsite.homefolder.homefolder import Members


class Index(TablePage):
    grok.title(u'Mein Ordner')
    grok.context(IMyHomeFolder)
    grok.implements(IFolderListingTable)
    #uvcsite.sectionmenu(uvcsite.IExtraViews)

    cssClasses = {'table': 'tablesorter zebra-striped'}
    cssClassEven = u'even'
    cssClassOdd = u'odd'

    startBachtAt = 15
    bachtSize = 15

    @property
    def title(self):
        name = self.request.principal.title
        return _(u"Ordner von %s", name)

    description = _(u"Hier werden Ihre Dokumente abgelegt")

    def getContentTypes(self):
        interaction = self.request.interaction
        for key, value in self.context.items():
            if interaction.checkPermission('uvc.ViewContent', value) and not getattr(value, 'excludeFromNav', False):
                yield dict(href = absoluteURL(value, self.request),
                           name = key) 

    def executeDelete(self, item):
        self.flash(_(u'Ihre Dokumente wurden entfernt'))
        del item.__parent__[item.__name__]

    def update(self): 
        items = self.request.form.get('table-checkBox-0-selectedItems')
        if items and self.request.has_key('form.button.delete'):
            if isinstance(items, (str, unicode)):
                items = [items,]
            for key in items:
                for pf in self.context.values():
                    if pf.has_key(key):
                        self.executeDelete(pf[key])
        super(Index, self).update()
        

class DirectAccess(grok.Viewlet):
    grok.view(IFolderListingTable)
    grok.order(25)
    grok.context(Interface)
    grok.viewletmanager(interfaces.IAboveContent)

    def getContentTypes(self):
        interaction = self.request.interaction
        items = self.context.items()
        if uvcsite.IProductFolder.providedBy(self.context):
            items = self.context.__parent__.items()
        for key, value in items:
            if interaction.checkPermission('uvc.ViewContent', value) and not getattr(value, 'excludeFromNav', False):
                yield dict(href = absoluteURL(value, self.request),
                           name = key) 


class HomeFolderValues(Values):
    """This Adapter returns IContent Objects
       form child folders
    """
    grok.adapts(IMyHomeFolder, None, Index)

    @property
    def values(self):
        results = []
        interaction = self.request.interaction
        for productfolder in self.context.values():
            if interaction.checkPermission('uvc.ViewContent', productfolder):
                results.extend(productfolder.values())
        return results


class RedirectIndexMembers(grok.View):
    grok.context(Members)
    grok.name('index')

    def render(self):
        url = uvcsite.IGetHomeFolderUrl(self.request).getURL()
        self.redirect(url)

