import grok

from hurry.workflow import workflow
from hurry.workflow.interfaces import IWorkflow
from hurry.workflow.interfaces import IWorkflowState
from hurry.workflow.interfaces import IWorkflowInfo

from hurry.query.query import Query
from hurry.query import Eq

from uvcsite.interfaces import IContentType
from uvcsite.workflow.transitions import create_workflow

class Workflow(grok.GlobalUtility, workflow.Workflow):
    grok.provides(IWorkflow)

    def __init__(self):
        super(Workflow, self).__init__(create_workflow())


class Versions(grok.GlobalUtility, workflow.WorkflowVersions):

    def getVersions(self, state, id):
        q = Query()
        return q.searchResults(
            Eq(('entry_catalog', 'workflow_state'),
               state) &
            Eq(('entry_catalog', 'workflow_id'),
               id))

    def getVersionsWithAutomaticTransitions(self):
        return []

    def hasVersion(self, id, state):
        return bool(len(self.getVersions(state, id)))

    def hasVersionId(self, id):
        q = Query()
        result = q.searchResults(
            Eq(('entry_catalog', 'workflow_id'), id))
        return bool(len(result))



class WorkflowState(grok.Adapter, workflow.WorkflowState):
    grok.context(IContentType)
    grok.provides(IWorkflowState)


class WorkflowInfo(grok.Adapter, workflow.WorkflowInfo):
    grok.context(IContentType)
    grok.provides(IWorkflowInfo)

