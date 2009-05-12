import grok
from uvcsite.helpsystem.interfaces import IHelpFolder, IHelpPage


class HelpPage(grok.Model):
    grok.implements(IHelpPage)

    def __init__(self, name, title="", text=""):
	self.name = name
	self.title = title
	self.text = text

class HelpAdd(grok.AddForm):
    grok.context(IHelpFolder)
    form_fields = grok.Fields(IHelpPage)
    template = grok.PageTemplateFile('templates/form.pt')

    @grok.action(u"Anlegen")
    def handle_add(self, **data):
	container = self.context
	helppage = HelpPage()
	self.applyData(helppage, **data)
	container[data.get('title')] = helppage
	self.redirect(self.url(helppage, 'overview'))

class HelpPageIndex(grok.DisplayForm):
    grok.name('overview')
    grok.context(IHelpPage)
    form_fields = grok.Fields(IHelpPage)
    template = grok.PageTemplateFile('templates/display_form.pt')


class TTDisplay(grok.View):
    grok.name('index')
    grok.context(HelpPage)


