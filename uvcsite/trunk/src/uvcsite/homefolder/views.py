# -*- coding: utf-8 -*- 
# Copyright (c) 2007-2008 NovaReto GmbH 
# cklinger@novareto.de 

import grok

from uvcsite import uvcsiteMF as _
from uvcsite.interfaces import IHomeFolder
from megrok.z3ctable import (TablePage, Column, GetAttrColumn,
	    CheckBoxColumn, LinkColumn, ModifiedColumn, Values)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState


class Index(TablePage):
    grok.context(IHomeFolder)

    cssClasses = {'table': 'listing'}
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
    grok.context(IHomeFolder)
    """ Delete the DATA"""

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
    grok.adapts(IHomeFolder, None, Index)

    @property
    def values(self):
        results = []
        for object in self.context.values():
            results.extend(object.values())
        return results


class CheckBox(CheckBoxColumn):
    grok.name('checkBox')
    grok.adapts(None, None, Index)
    weight = 0


class Link(LinkColumn):
    grok.name('link')
    grok.adapts(None, None, Index)
    weight = 1
    header = u"edit"
    linkName = u"edit"
    linkContent = u"edit this item"


class MetaTypeColumn(GetAttrColumn):
    grok.name('meta_type')
    grok.adapts(IHomeFolder, None, Index)
    header = _(u'Object')
    attrName = 'meta_type'
    weight = 2

    
class StateColumn(GetAttrColumn):
    grok.name('state')
    grok.adapts(IHomeFolder, None, Index)
    header = _(u'Status')
    attrName = 'status'
    weight = 3 
    
    def getValue(self, obj):
        state = IWorkflowState(obj).getState()
        if state != None:
            return titleForState(state)
        return self.defaultValue
   

class CreatorColumn(Column):
    grok.name('creator')
    header = u"Autor"
    weight = 4  
    grok.adapts(IHomeFolder, None, Index)
    
    def renderCell(self, item):
        return ', '.join(IZopeDublinCore(item).creators)


class ModifiedColumn(ModifiedColumn):
    grok.name('modified')
    header = u"Datum"
    weight = 4  
    grok.adapts(IHomeFolder, None, Index)
    
