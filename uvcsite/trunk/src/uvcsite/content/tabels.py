import grok

from uvcsite import uvcsiteMF as _
from megrok.z3ctable import (TablePage, Column, GetAttrColumn,
            CheckBoxColumn, LinkColumn, ModifiedColumn, Values)

from hurry.workflow.interfaces import IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore
from uvcsite.workflow.basic_workflow import titleForState
from uvcsite.interfaces import IFolderColumnTable

class CheckBox(CheckBoxColumn):
    grok.name('checkBox')
    grok.adapts(IFolderColumnTable, None, None)
    weight = 0
    cssClasses = {'th': 'checkBox'}
    header = u""


class Link(LinkColumn):
    grok.name('link')
    grok.adapts(IFolderColumnTable, None, None)
    weight = 1
    header = _(u"Titel")
    linkName = u"edit"

    def getLinkContent(self, item):
        return item.title


class MetaTypeColumn(GetAttrColumn):
    grok.name('meta_type')
    grok.adapts(IFolderColumnTable, None, None)
    header = _(u'Objekt')
    attrName = 'meta_type'
    weight = 2


class CreatorColumn(Column):
    grok.name('creator')
    header = _(u"Autor")
    weight = 99
    grok.adapts(IFolderColumnTable, None, None)

    def renderCell(self, item):
        return ', '.join(IZopeDublinCore(item).creators)


class ModifiedColumn(ModifiedColumn):
    grok.name('modified')
    header = _(u"Datum")
    weight = 100
    grok.adapts(IFolderColumnTable, None, None)
