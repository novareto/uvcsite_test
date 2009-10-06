from uvcsite.content import (ProductFolder, IProductFolder, contenttype,
                         IContent, Content, icon, schema, name)
from zope.i18nmessageid import MessageFactory
uvcsiteMF = MessageFactory('uvcsite')
from megrok.layout import Page
from uvcsite.content import ApplicationAwareView

class Page(Page, ApplicationAwareView):
    grok.baseclass()
