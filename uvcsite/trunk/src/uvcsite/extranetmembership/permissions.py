import grok

class ManageMitbenutzer(grok.Role):
    grok.name('uvc.ManageMitbenutzer')
    grok.permissions('uvc.CanManageMitbenutzer')


# Permissions
class CanManageMitbenutzer(grok.Permission):
    grok.name('uvc.CanManageMitbenutzer')  
