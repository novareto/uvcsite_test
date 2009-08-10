import grok

from uvcsite import uvcsiteMF as _
from grok.interfaces import IContainer
from megrok.z3ctable import (TablePage, Column, GetAttrColumn,
            CheckBoxColumn, LinkColumn, ModifiedColumn, Values)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState


class CheckBox(CheckBoxColumn):
    grok.name('checkBox')
    grok.adapts(IContainer, None, None)
    weight = 0


class Link(LinkColumn):
    grok.name('link')
    grok.adapts(IContainer, None, None)
    weight = 1
    header = u"edit"
    linkName = u"edit"
    linkContent = u"edit this item"


class MetaTypeColumn(GetAttrColumn):
    grok.name('meta_type')
    grok.adapts(IContainer, None, None)
    header = _(u'Object')
    attrName = 'meta_type'
    weight = 2


class CreatorColumn(Column):
    grok.name('creator')
    header = u"Autor"
    weight = 99 
    grok.adapts(IContainer, None, None)

    def renderCell(self, item):
        return ', '.join(IZopeDublinCore(item).creators)


class ModifiedColumn(ModifiedColumn):
    grok.name('modified')
    header = u"Datum"
    weight = 100 
    grok.adapts(IContainer, None, None)
