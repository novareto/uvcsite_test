# -*- coding: utf-8 -*-

import grok
import zope.interface
import uvcsite.content
import hurry.workflow
import zope.dublincore.interfaces

from uvcsite import IUVCSite
from zope.component.interfaces import ObjectEvent, IObjectEvent

from .events import ICatalogDeployment



class IApplicationContent(zope.interface.Interface):

    type = zope.interface.Attribute('Content type')
    state = zope.interface.Attribute('Workflow state')
    modification_date = zope.interface.Attribute('Workflow state')


@zope.interface.implementer(IApplicationContent)
class ApplicationContent(grok.Adapter):
    grok.context(uvcsite.content.interfaces.IContent)

    @property
    def type(self):
        return self.context.__class__.__name__

    @property
    def state(self):
        wfstate = hurry.workflow.interfaces.IWorkflowState(self.context)
        return wfstate.getState()

    @property
    def modification_date(self):
        dates = zope.dublincore.interfaces.IDCTimes(self.context)
        return dates.modified


class WorkflowCatalog(grok.Indexes):
    grok.context(IApplicationContent)
    grok.name('workflow_catalog')
    grok.site(IUVCSite)
    grok.install_on(ICatalogDeployment)

    type = grok.index.Field()
    state = grok.index.Field()
    modification_date = grok.index.Datetime()
