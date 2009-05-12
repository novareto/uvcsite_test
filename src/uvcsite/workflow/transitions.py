from datetime import datetime
from hurry.workflow import workflow

CREATED = 0
PUBLISHED = 1

def reverseStates(state):
    mapping = {'0':'Entwurf', '1':'gesendet'}
    return mapping.get(str(state), 'unbekannt')

def publish_action(info, context):
    context.published = datetime.now()

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
        destination=PUBLISHED,
        action=publish_action)

    update_transition = workflow.Transition(
        transition_id='update',
        title='update',
        source=PUBLISHED,
        destination=PUBLISHED,
        action=publish_action)

    return [create_transition, publish_transition, update_transition]
