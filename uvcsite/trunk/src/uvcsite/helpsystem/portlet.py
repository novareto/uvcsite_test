import grok
from zope.interface import Interface
from uvcsite.interfaces import IHelp

class HelpPortlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IHelp)
    grok.baseclass()

    urls=[
            {'href': 'hilfe', 'name': 'zur Eingabemaske'},
	 ]
