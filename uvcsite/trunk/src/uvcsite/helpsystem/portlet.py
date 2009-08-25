import grok
from zope.interface import Interface
from uvcsite.interfaces import IHelp


class HelpPortlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IHelp)
    grok.baseclass()
    template = grok.PageTemplateFile('templates/helpportlet.pt')

    urls = []

    def render(self):
        return self.template.render(self)
