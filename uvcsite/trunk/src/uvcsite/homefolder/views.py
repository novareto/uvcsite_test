# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from zope.component import Interface
from uvcsite import uvcsiteMF as _
from uvcsite import ApplicationAwareView 
from uvcsite.interfaces import IMyHomeFolder
from megrok.z3ctable import (TablePage, Column, GetAttrColumn,
            CheckBoxColumn, LinkColumn, ModifiedColumn, Values, table)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState
from uvcsite.interfaces import IFolderColumnTable
from megrok.z3cform.tabular import DeleteFormTablePage


class Index(DeleteFormTablePage, ApplicationAwareView):
    grok.context(IMyHomeFolder)

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
        return self.context.keys()

    def executeDelete(self, item):
        self.flash(u'Ihre Dokumente wurden entfernt')
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
