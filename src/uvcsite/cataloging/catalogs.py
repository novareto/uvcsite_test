import grok
import zope.interface
import uvcsite.content
import hurry.workflow
from uvcsite import IUVCSite
from zope.component.interfaces import ObjectEvent, IObjectEvent


class ICatalogDeployment(IObjectEvent):
    pass


@zope.interface.implementer(ICatalogDeployment)
class CatalogDeployment(ObjectEvent):
    pass


class IApplicationContent(zope.interface.Interface):

    type = zope.interface.Attribute('Content type')
    state = zope.interface.Attribute('Workflow state')


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


class WorkflowCatalog(grok.Indexes):
    grok.context(IApplicationContent)
    grok.name('workflow_catalog')
    grok.site(IUVCSite)
    grok.install_on(grok.IApplicationAddedEvent)

    type = grok.index.Field()
    state = grok.index.Field()
