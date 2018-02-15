"""
Content
=======

:doctest:

Setup
-----

We have to grok some components first...

  >>> import grok
  >>> grok.grok('uvcsite.tests.functional.content.multiple_workflow')

First start with makeing an instance of the Content

  >>> from uvcsite.app import Uvcsite
  >>> r = getRootFolder()
  >>> r['folder'] = folder = Uvcsite()
  >>> folder
  <uvcsite.app.Uvcsite object at ...>

  >>> from zope.component import getUtility
  >>> wf = getUtility(IWorkflow, name="special")
  >>> wf
  <hurry.workflow.workflow.Workflow object at ...>

  >>> content = SpecialContent()
  >>> content
  <...SpecialContent object at ...>

  >>> r['folder']['hans'] = content

  >>> from hurry.workflow.interfaces import IWorkflowState
  >>> wf = IWorkflowState(content)
  >>> wf.getState()
  666
"""

from grokcore.component import Adapter
from grokcore.component import name, provides, context, global_utility
from uvcsite import content
from zope.interface import implementer
from hurry.workflow.interfaces import *
from hurry.workflow import workflow
from zope.schema import TextLine, Int


class ISpecialContent(content.IContent):
    pass


@implementer(ISpecialContent)
class SpecialContent(content.Content):
    content.schema(ISpecialContent)
    content.name('MyContent')


class WorkflowState(workflow.WorkflowState, Adapter):
    context(ISpecialContent)
    provides(IWorkflowState)
    name("special")


class WorkflowInfo(workflow.WorkflowInfo, Adapter):
    context(ISpecialContent)
    provides(IWorkflowInfo)
    name = 'special'


create_transition = workflow.Transition(
    transition_id='create',
    title='create',
    source=None,
    destination=666)


global_utility(workflow.Workflow([create_transition]),
               provides=IWorkflow,
               name="special",
               direct=True)
