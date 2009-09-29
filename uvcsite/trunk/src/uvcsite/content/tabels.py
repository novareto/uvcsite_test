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
    grok.context(IFolderColumnTable)
    weight = 0
    cssClasses = {'th': 'checkBox'}
    header = u""


class Link(LinkColumn):
    grok.name('link')
    grok.context(IFolderColumnTable)
    weight = 1
    header = _(u"Titel")
    linkName = u"edit"

    def getLinkContent(self, item):
        return item.title


class MetaTypeColumn(GetAttrColumn):
    grok.name('meta_type')
    grok.context(IFolderColumnTable)
    header = _(u'Objekt')
    attrName = 'meta_type'
    weight = 2


class CreatorColumn(Column):
    grok.name('creator')
    grok.context(IFolderColumnTable)
    header = _(u"Autor")
    weight = 99

    def renderCell(self, item):
        return ', '.join(IZopeDublinCore(item).creators)


class ModifiedColumn(ModifiedColumn):
    grok.name('modified')
    grok.context(IFolderColumnTable)
    header = _(u"Datum")
    weight = 100
