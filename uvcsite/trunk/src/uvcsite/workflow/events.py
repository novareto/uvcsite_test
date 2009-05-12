import grok
from zope.schema import getFields
from uvcsite.interfaces import IContentType
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState
from zope.dublincore.interfaces import IZopeDublinCore

@grok.subscribe(IContentType, grok.IObjectAddedEvent)
def initializeWorkflow(content, event):
    """ Setting the InitialStatus of the Workflow """
    IWorkflowInfo(content).fireTransition('create')
