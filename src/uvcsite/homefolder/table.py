# -*- coding: utf-8 -*-

import grok
from z3c.table import table, column, header, value

from uvcsite import uvcsiteMF as _
from zope.interface import Interface
from z3c.table.interfaces import IValues, IColumn, ITable, IColumnHeader
from hurry.workflow.interfaces import IWorkflowState
from uvcsite.workflow.basic_workflow import titleForState
from uvcsite.interfaces import IHomeFolder

from zope.dublincore.interfaces import IZopeDublinCore

class IHFTable(Interface):
    """ Markter Interface for IHFTable"""

class HFTable(table.Table, grok.View):
    grok.implements(IHFTable)
    grok.name('table')
    grok.context(IHomeFolder)


    cssClasses = {'table': 'listing',
                  'thead': 'thead'}

    cssClassEven = u'even'
    cssClassOdd = u'odd'

    startBatchingAt = 15 
    batchSize = 15 



class SortingHeader(grok.MultiAdapter, header.SortingColumnHeader):
    grok.implements(IColumnHeader)
    grok.provides(IColumnHeader)
    grok.adapts(IHomeFolder, Interface, HFTable, IColumn)


class CustomValues(grok.MultiAdapter, value.ValuesForContainer):
    grok.implements(IValues)
    grok.provides(IValues)
    grok.adapts(IHomeFolder, Interface, HFTable)

    @property
    def values(self):
        results = []
	for object in self.context.values():
	    results.extend(object.values())
	meta_type = self.request.get('meta_type', None)
	if meta_type:
            results = [x for x in results if x.meta_type == meta_type]
	return results 

class HakenColumn(grok.MultiAdapter, column.CheckBoxColumn):
    grok.name('checkbox')
    grok.implements(IColumn)
    grok.provides(IColumn)
    grok.adapts(IHomeFolder, Interface, HFTable)

    header = u' '
    weight = 0

class FirstNameColumn(grok.MultiAdapter, column.Column):
    grok.name('firstName')
    grok.implements(IColumn)
    grok.provides(IColumn)
    grok.adapts(IHomeFolder, Interface, HFTable)

    header = _(u'Name')
    weight = 1

    def renderCell(self, item):
	url = grok.url( self.request, item, name="index") 
	return '<a href="%s"> %s </a>' %(url, item.name)

    def getSortKey(self, item):
	return item.name

class MetaTypeColumn(grok.MultiAdapter, column.GetAttrColumn):
    grok.name('meta_type')
    grok.implements(IColumn)
    grok.provides(IColumn)
    grok.adapts(IHomeFolder, Interface, HFTable)
    header = _(u'Object')
    attrName = 'meta_type'
    weight = 2


class StateColumn(grok.MultiAdapter, column.GetAttrColumn):
    grok.name('state')
    grok.implements(IColumn)
    grok.provides(IColumn)
    grok.adapts(IHomeFolder, Interface, HFTable)
    header = _(u'Status')
    attrName = 'status'
    weight = 3 


    def getValue(self, obj):
	state = IWorkflowState(obj).getState()
	if state != None:
	    return titleForState(state)
        return self.defaultValue

class CreatorColumn(grok.MultiAdapter, column.Column):    
    grok.name('creator')
    header = u"Autor"
    weight = 4 
    grok.implements(IColumn)
    grok.provides(IColumn)
    grok.adapts(IHomeFolder, Interface, HFTable)

    def renderCell(self, item):
	return ', '.join(IZopeDublinCore(item).creators)

class ModifiedColumn(grok.MultiAdapter, column.ModifiedColumn):    
    grok.name('modified')
    grok.implements(IColumn)
    grok.provides(IColumn)
    grok.adapts(IHomeFolder, Interface, HFTable)
