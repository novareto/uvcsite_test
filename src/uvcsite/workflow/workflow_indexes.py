import grok
from grok import index
from uvcsite.interfaces import IUVCSite
from hurry.workflow.interfaces import IWorkflowState

class WorkflowIndexes(grok.Indexes):
    grok.site(IUVCSite)
    grok.context(IWorkflowState)
    grok.name('entry_catalog')

    workflow_state = index.Field(attribute='getState')
    workflow_id = index.Field(attribute='getId')

