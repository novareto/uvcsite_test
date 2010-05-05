"""
Content
=======

Setup
-----

First start with makeing an instance of the Content 

  >>> from uvcsite.app import Uvcsite
  >>> from zope.app.testing.functional import getRootFolder
  >>> r = getRootFolder()
  >>> r['folder'] = folder = Uvcsite()
  >>> folder
  <uvcsite.app.Uvcsite object at ...>

  >>> from zope.site.hooks import setSite
  >>> setSite(folder)

  >>> content = SpecialContent() 
  >>> content 
  <uvcsite.content.ftests.multiple_workflow.SpecialContent object at 0...>

  >>> r['folder']['hans'] = content

  >>> from hurry.workflow.interfaces import IWorkflowState
  >>> wf = IWorkflowState(content)   
  >>> wf.getState()
  666
"""

import grok
from uvcsite import content
from zope.schema import TextLine, Int
from hurry.workflow import workflow
from hurry.workflow.interfaces import *

class ISpecialContent(content.IContent):
    name = TextLine(title = u"Name")
    age = Int(title = u"Int")


class SpecialContent(content.Content):
    grok.implements(ISpecialContent)
    content.schema(ISpecialContent)
    content.name('MyContent')


def create_workflow(): 
    """ Basic Setup For Workflow Utility""" 
    create_transition = workflow.Transition( 
        transition_id='create', 
        title='create', 
        source=None, 
        destination=666) 
 
 
    return workflow.Workflow([create_transition,]) 
 
grok.global_utility(create_workflow, name="special", provides=IWorkflow) 


class WorkflowState(workflow.WorkflowState, grok.Adapter):
    grok.context(ISpecialContent)
    grok.provides(IWorkflowState)
    grok.name("special")
    name = 'special'

# Workflow Info

class WorkflowInfo(workflow.WorkflowInfo, grok.Adapter):
    grok.context(ISpecialContent)
    grok.provides(IWorkflowInfo)
    name = 'special'
