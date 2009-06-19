import grok

# Roles
class MasterUser(grok.Role):
    grok.name('uvc.MasterUser')
    grok.permissions('uvc.ManageCoUsers')


# Permissions
class ManageCoUsers(grok.Permission):
    grok.name('uvc.ManageCoUsers')  
