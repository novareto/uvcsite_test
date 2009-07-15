import grok
from megrok.layout.components import Form
from uvcsite.helpsystem.interfaces import IHelpFolder, IHelpPage


class HelpPage(grok.Model):
    grok.implements(IHelpPage)

    def __init__(self, name="", title="", text=""):
	self.name = name
	self.title = title
	self.text = text

class HelpAdd(Form, grok.AddForm):
    grok.context(IHelpFolder)
    form_fields = grok.Fields(IHelpPage)

    @grok.action(u"Anlegen")
    def handle_add(self, **data):
	container = self.context
	helppage = HelpPage()
	self.applyData(helppage, **data)
	container[data.get('title')] = helppage
	self.redirect(self.url(helppage, 'overview'))

class HelpPageIndex(Form, grok.DisplayForm):
    grok.name('overview')
    grok.context(IHelpPage)
    form_fields = grok.Fields(IHelpPage)


class TTDisplay(grok.View):
    grok.name('index')
    grok.context(HelpPage)


