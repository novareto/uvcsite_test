# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
from uvcsite import uvcsiteMF as _
from uvcsite.interfaces import IMyHomeFolder, IFolderListingTable
from megrok.z3ctable import Values
from megrok.z3cform.tabular import DeleteFormTablePage
from zope.traversing.browser import absoluteURL


class Index(DeleteFormTablePage):
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
