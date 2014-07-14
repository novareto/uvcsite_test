# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import uvclight

from dolmen.content import IContent
from datetime import datetime
from zope.lifecycleevent import IObjectAddedEvent
from grokcore.component import subscribe, global_utility
from hurry.workflow import workflow
from hurry.workflow.interfaces import IWorkflow, IWorkflowState
from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowTransitionEvent


CREATED = 0
PUBLISHED = 1
PROGRESS = 2


def titleForState(state):
    """ Reverse Mapping of workflow States """
    mapping = {0: 'Entwurf', 1: 'gesendet', 2: 'in Verarbeitung'}
    return mapping.get(state, 'unbekannt')


def create_workflow():
    """ Basic Setup For Workflow Utility"""
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

    progress_transition = workflow.Transition(
        transition_id='progress',
        title='progress',
        source=CREATED,
        destination=PROGRESS)

    fix_transition = workflow.Transition( 
        transition_id='fix',
        title='fix',
        source=PROGRESS,
        destination=PUBLISHED)

    return workflow.Workflow([create_transition,
                              progress_transition,
                              fix_transition,
                              publish_transition])

global_utility(create_workflow, provides=IWorkflow)


# Workflow States

class WorkflowState(workflow.WorkflowState, uvclight.Adapter):
    uvclight.context(IContent)
    uvclight.provides(IWorkflowState)

# Workflow Info

class WorkflowInfo(workflow.WorkflowInfo, uvclight.Adapter):
    uvclight.context(IContent)
    uvclight.provides(IWorkflowInfo)

# Events


@subscribe(IContent, IObjectAddedEvent)
def initializeWorkflow(content, event):
    IWorkflowInfo(content).fireTransition('create')


@subscribe(IWorkflowTransitionEvent)
def set_publish_action(event):
    event.object.published = datetime.now()
