# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from uvcsite import IContent
from datetime import datetime
from zc.blist import BList

from hurry.workflow import workflow
from hurry.workflow.interfaces import (
    IWorkflow, IWorkflowState, IWorkflowInfo, IWorkflowTransitionEvent)


CREATED = 0
PUBLISHED = 1


def titleForState(state):
    """ Reverse Mapping of workflow States """
    mapping = {0: 'Entwurf', 1: 'gesendet'}
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

    return workflow.Workflow([create_transition,
                              publish_transition])

grok.global_utility(create_workflow, provides=IWorkflow)


# Workflow Versions (Not sure if really needed!!!)


class MyWorkflowVersions(grok.GlobalUtility, workflow.WorkflowVersions):
    """ Worklfow Versions is needed by hurry Workflow
        This is a really basic impplementation and
        should be replaced with a better one"""

    def __init__(self):
        self.clear()

    def addVersion(self, obj):
        """ """
        self.versions.append(obj)

    def getVersions(self, state, id):
        """ """
        result = []
        for version in self.versions:
            state_adapter = IWorkflowState(version)
            if state_adapter.getId() == id and state_adapter.getState() == state:
                result.append(version)
        return result

    def getVersionsWithAutomaticTransitions(self):
        """ """
        result = []
        for version in self.versions:
            if IWorkflowInfo(version).hasAutomaticTransitions():
                result.append(version)
        return result

    def hasVersion(self, state, id):
        """ """
        return bool(self.getVersions(state, id))

    def hasVersionId(self, id):
        """ """
        for version in self.versions:
            state_adapter = IWorkflowState(version)
            if state_adapter.getId() == id:
                return True
        return False

    def clear(self):
        """ """
        self.versions = BList()

# Workflow States


class WorkflowState(grok.Adapter, workflow.WorkflowState):
    grok.context(IContent)
    grok.provides(IWorkflowState)


class WorkflowInfo(grok.Adapter, workflow.WorkflowInfo):
    grok.context(IContent)
    grok.provides(IWorkflowInfo)

# Events


@grok.subscribe(IContent, grok.IObjectAddedEvent)
def initializeWorkflow(content, event):
    IWorkflowInfo(content).fireTransition('create')


@grok.subscribe(IWorkflowTransitionEvent)
def set_publish_action(event):
    event.object.published = datetime.now()
