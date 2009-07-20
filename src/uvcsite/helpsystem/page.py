import grok

from uvcsite.content.base import Content
from megrok.layout.components import Form
from uvcsite.helpsystem.interfaces import IHelpFolder, IHelpPage


class HelpPage(Content):
    grok.implements(IHelpPage)

    def __init__(self, name="", title="", text=""):
	self.name = name
	self.title = title
	self.text = text


class HelpAdd(Form, grok.AddForm):
    grok.context(IHelpFolder)
    form_fields = grok.Fields(IHelpPage)
    grok.require('zope.ManageSite')

    @grok.action(u"Anlegen")
    def handle_add(self, **data):
	container = self.context
	helppage = HelpPage()
	self.applyData(helppage, **data)
	container[data.get('title')] = helppage
	self.flash(u'Die Hilfeseite wurde erfolgreich angelegt')
	self.redirect(self.url(helppage, 'overview'))


class Edit(Form, grok.EditForm):
    grok.context(IHelpPage)
    form_fields = grok.Fields(IHelpPage)
    grok.require('zope.ManageSite')


class HelpPageIndex(Form, grok.DisplayForm):
    grok.name('overview')
    grok.context(IHelpPage)
    form_fields = grok.Fields(IHelpPage)


class TTDisplay(grok.View):
    grok.name('index')
    grok.context(HelpPage)
