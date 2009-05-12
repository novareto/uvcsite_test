import grok
from uvcsite.helpsystem.interfaces import IHelpFolder
from zope.app.authentication.interfaces import IPrincipal

class HelpFolder(grok.Container):
    grok.implements(IHelpFolder)

    def traverse(self, name):
	if not name in self:
	    return self['keineHilfe'] 
        return self[name]

class HelpFolderIndex(grok.View):
    grok.name('index')
    pass


