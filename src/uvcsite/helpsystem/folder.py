import grok
import megrok.layout

from uvcsite.interfaces import IUVCSite
from uvcsite.helpsystem.interfaces import IHelpFolder
from zope.app.authentication.interfaces import IPrincipal


class HelpFolder(grok.Container):
    grok.implements(IHelpFolder)


class Index(megrok.layout.Page):
    pass


@grok.subscribe(IUVCSite, grok.IObjectAddedEvent)
def addHelpFolder(context, event):
    context['hilfe'] = HelpFolder()
