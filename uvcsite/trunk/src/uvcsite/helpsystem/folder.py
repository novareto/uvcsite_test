import grok
import megrok.layout

from uvcsite.helpsystem.interfaces import IHelpFolder
from zope.app.authentication.interfaces import IPrincipal

class HelpFolder(grok.Container):
    grok.implements(IHelpFolder)

class HelpFolderIndex(megrok.layout.Page):
    grok.name('index')
    pass


