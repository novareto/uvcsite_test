# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
from uvcsite import uvcsiteMF as _
from megrok.z3ctable import Values
from megrok.z3ctable import TablePage
from zope.traversing.browser import absoluteURL
from uvcsite.interfaces import IMyHomeFolder, IFolderListingTable
from uvc.layout import interfaces


class Index(TablePage):
    grok.context(IMyHomeFolder)
    grok.implements(IFolderListingTable)

    cssClasses = {'table': 'tablesorter myTable'}
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
        for key, value in self.context.items():
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
    grok.view(Index)
    grok.order(25)
    grok.context(IMyHomeFolder)
    grok.viewletmanager(interfaces.IAboveContent)


class HomeFolderValues(Values):
    """This Adapter returns IContent Objects
       form child folders
    """
    grok.adapts(IMyHomeFolder, None, Index)

    @property
    def values(self):
        results = []
        for object in self.context.values():
            results.extend(object.values())
        return results
