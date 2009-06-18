import grok

from hurry.workflow import workflow
from hurry.workflow.interfaces import IWorkflow
from hurry.workflow.interfaces import IWorkflowState
from hurry.workflow.interfaces import IWorkflowInfo
from hurry.workflow.interfaces import IWorkflowTransitionEvent

from hurry.query.query import Query
from hurry.query import Eq

from uvcsite.interfaces import IContentType

from persistent.list import PersistentList
from datetime import datetime


CREATED = 0
PUBLISHED = 1

def titleForState(state):
    mapping = {0:'Entwurf', 1:'gesendet'}
    return mapping.get(state, 'unbekannt')

@grok.subscribe(IWorkflowTransitionEvent)
def set_publish_action(event):
    event.object.published = datetime.now()



def create_workflow():
    create_transition = workflow.Transition(
        transition_id='create',
        title='create',
        source=None,
        destination=CREATED)

    publish_transition = workflow.Transition(
        transition_id='publish',
        title='publish',
        source=CREATED,
        destination=PUBLISHED)

    return workflow.Workflow([create_transition, 
                              publish_transition])

grok.global_utility(create_workflow, provides=IWorkflow)
class MyWorkflowVersions(grok.GlobalUtility, workflow.WorkflowVersions):
    
    def __init__(self):
        self.clear() 

    def addVersion(self, obj):
        self.versions.append(obj)

    def getVersions(self, state, id):
        result = []
        for version in self.versions:
            state_adapter = interfaces.IWorkflowState(version)
            if state_adapter.getId() == id and state_adapter.getState() == state:
                result.append(version)
        return result

    def getVersionsWithAutomaticTransitions(self):
        result = []
        for version in self.versions:
            if interfaces.IWorkflowInfo(version).hasAutomaticTransitions():
                result.append(version)
        return result

    def hasVersion(self, state, id):
        return bool(self.getVersions(state, id))

    def hasVersionId(self, id):
        result = []
        for version in self.versions:
            state_adapter = interfaces.IWorkflowState(version)
            if state_adapter.getId() == id:
                return True
        return False

    def clear(self):
        self.versions = PersistentList() 


class WorkflowState(grok.Adapter, workflow.WorkflowState):
    grok.context(IContentType)
    grok.provides(IWorkflowState)


class WorkflowInfo(grok.Adapter, workflow.WorkflowInfo):
    grok.context(IContentType)
    grok.provides(IWorkflowInfo)

@grok.subscribe(IContentType, grok.IObjectAddedEvent)
def initializeWorkflow(content, event):
    IWorkflowInfo(content).fireTransition('create')
