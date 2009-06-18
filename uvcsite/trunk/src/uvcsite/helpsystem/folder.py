import grok
import megrok.pagelet

from uvcsite.helpsystem.interfaces import IHelpFolder
from zope.app.authentication.interfaces import IPrincipal

class HelpFolder(grok.Container):
    grok.implements(IHelpFolder)

class HelpFolderIndex(megrok.pagelet.Pagelet):
    grok.name('index')
    pass


