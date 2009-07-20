import grok
import megrok.z3ctable

from uvcsite import uvcsiteMF as _
from zope.interface import Interface
from uvcsite.viewlets.utils import MenuItem
from uvcsite.interfaces import IUVCSite, IGlobalMenu
from uvcsite.helpsystem.interfaces import IHelpFolder
from zope.app.authentication.interfaces import IPrincipal


class HelpFolder(grok.Container):
    grok.implements(IHelpFolder)


class Index(megrok.z3ctable.TablePage):
    grok.require('zope.ManageSite')


class Hilfe(MenuItem):
    grok.name(_(u'Hilfe'))
    grok.context(Interface)
    grok.viewletmanager(IGlobalMenu)
    grok.require('zope.ManageSite')

    title= _(u'Hilfe')
    urlEndings = "hilfe"
    viewURL = "hilfe"


@grok.subscribe(IUVCSite, grok.IObjectAddedEvent)
def addHelpFolder(context, event):
    context['hilfe'] = HelpFolder()
