# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import uvclight
import uvcsite

from uvcsite import uvcsiteMF as _
from megrok.z3ctable import (table,
    Column, GetAttrColumn, CheckBoxColumn, LinkColumn, ModifiedColumn)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState
from uvcsite.interfaces import IFolderColumnTable, IFolderListingTable
from zope.traversing.browser import absoluteURL
from uvcsite.homefolder.views import Index
from datetime import timedelta


class CheckBox(CheckBoxColumn):
    uvclight.name('checkBox')
    uvclight.context(IFolderColumnTable)
    table(IFolderListingTable)

    weight = 0
    cssClasses = {'th': 'checkBox'}
    header = u""

    def renderCell(self, item):
        state = IWorkflowState(item).getState()
        if state != None:
            state = titleForState(state)
        if state == "Entwurf":
            return CheckBoxColumn.renderCell(self, item)
        return ''    


class Link(LinkColumn):
    uvclight.name('link')
    uvclight.context(IFolderColumnTable)
    table(IFolderListingTable)
    
    weight = 1
    header = _(u"Titel")
    linkName = u"edit"

    def getLinkURL(self, item):
        """Setup link url."""
        state = IWorkflowState(item).getState()
        if state != None:
            state = titleForState(state)
        if self.linkName is not None and state == "Entwurf":
            return '%s/%s' % (absoluteURL(item, self.request), self.linkName)
        return absoluteURL(item, self.request)

    def getLinkContent(self, item):
        return item.title


class MetaTypeColumn(GetAttrColumn):
    uvclight.name('meta_type')
    uvclight.context(IFolderColumnTable)
    header = _(u'Objekt')
    attrName = 'meta_type'
    weight = 2
    table(IFolderListingTable)


class CreatorColumn(Column):
    uvclight.name('creator')
    uvclight.context(IFolderColumnTable)
    table(IFolderListingTable)
    
    header = _(u"Autor")
    weight = 99

    def renderCell(self, item):
        return ', '.join(IZopeDublinCore(item).creators)


class ModifiedColumn(Column):
    uvclight.name('modified')
    uvclight.context(IFolderColumnTable)
    table(IFolderListingTable)
    
    header = _(u"Datum")
    weight = 100

    def getSortKey(self, item):
        return item.modtime

    def renderCell(self, item):
        return uvcsite.fmtDateTime(item.modtime)


class StateColumn(GetAttrColumn):
    uvclight.name('state')
    uvclight.context(IFolderColumnTable)
    table(IFolderListingTable)
    
    header = _(u'Status')
    attrName = 'status'
    weight = 3
    
    def getValue(self, obj):
        state = IWorkflowState(obj).getState()
        if state != None:
            return titleForState(state)
        return self.defaultValue
