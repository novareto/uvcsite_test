import grok


## Roles

class RolleMember(grok.Role):
    grok.name('uvc.RolleMember')
    grok.permissions('uvc.View')

class ManageHomeFolder(grok.Role):
    grok.name('uvc.ManageHomeFolder')
    grok.permissions('uvc.AccessHomeFolder')

class ManageKontakt(grok.Role):
    grok.name('uvc.ManageKontakt')
    grok.permissions('uvc.AccesHomeFolder', 'uvc.kontakt')

## Permissions

class View(grok.Permission):
    grok.name('uvc.View')

class AccessHomeFolder(grok.Permission):
    grok.name('uvc.AccessHomeFolder')

class EditKontakt(grok.Permission):
    grok.name('uvc.kontakt')
