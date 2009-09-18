# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from zope.component import Interface
from uvcsite import uvcsiteMF as _
from uvcsite import ApplicationAwareView 
from uvcsite.interfaces import IMyHomeFolder
from megrok.z3ctable import (TablePage, Column, GetAttrColumn,
            CheckBoxColumn, LinkColumn, ModifiedColumn, Values)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState


class Index(TablePage, ApplicationAwareView):
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


class DeleteItem(grok.View):
    """ Delete the DATA"""
    grok.context(Interface)

    def update(self):
        liste=[]
        context = self.context
        request = self.request
        items = request.get('table-checkBox-0-selectedItems', None)
        if items:
            if isinstance(items, (str, unicode)):
                liste.append(items)
            else:
                liste = items
            for x in liste:
                del context[str(x)]

    def render(self, **kw):
        self.flash(u'Die Objekte wurden gelöscht')
        self.redirect(self.url(self.context))


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


class StateColumn(GetAttrColumn):
    grok.name('state')
    grok.adapts(IMyHomeFolder, None, Index)
    header = _(u'Status')
    attrName = 'status'
    weight = 3

    def getValue(self, obj):
        state = IWorkflowState(obj).getState()
        if state != None:
            return titleForState(state)
        return self.defaultValue
