import grok
from zope.securitypolicy.interfaces import IRolePermissionManager
from uvcsite.workflow.basic_workflow import PUBLISHED
from hurry.workflow.interfaces import IWorkflowTransitionEvent


# Roles
class User(grok.Role):
    grok.name('uvc.User')
    grok.permissions('zope.View')

class Editor(grok.Role):
    grok.name('uvc.Editor')
    grok.permissions('uvc.AddContent', 'uvc.ViewContent', 'uvc.EditContent')


# Permissions
class View(grok.Permission):
    grok.name('uvc.ViewContent')  

class Add(grok.Permission):
    grok.name('uvc.AddContent')  

class Edit(grok.Permission):
    grok.name('uvc.EditContent') 


@grok.subscribe(IWorkflowTransitionEvent)
def remove_edit_permission(event):
    if event.destination != PUBLISHED:
        return
    IRolePermissionManager(event.object).denyPermissionToRole(
           'uvc.EditContent', 'uvc.Editor')
