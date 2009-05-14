import grok

class ManageKontakt(grok.Role):
    grok.name('uvc.ManageKontakt')
    grok.permissions('uvc.AccesHomeFolder', 'uvc.CanAddKontakt')


# Permissions
class CanViewKontakt(grok.Permission):
    grok.name('uvc.CanViewKontakt')  

class CanAddKontakt(grok.Permission):
    grok.name('uvc.CanAddKontakt')  

class CanEditKontakt(grok.Permission):
    grok.name('uvc.CanEditKontakt')  
