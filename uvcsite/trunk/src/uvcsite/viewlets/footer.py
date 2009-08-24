import grok
from zope.interface import Interface
from uvcsite.interfaces import IFooter
from uvcsite.viewlets.utils import MenuItem

class Impressum(MenuItem):
    grok.name(u'Impressum')
    grok.context(Interface)
    grok.viewletmanager(IFooter)
    grok.order(1)

    urlEndings = "impressum"
    viewURL = "impressum"

class Barrierefreiheit(MenuItem):
    grok.name(u'Barrierefreiheit')
    grok.context(Interface)
    grok.viewletmanager(IFooter)
    grok.order(2)

    urlEndings = "barrierefreiheit"
    viewURL = "barrierefreiheit"

class Kontakt(MenuItem):
    grok.name(u'Kontakt')
    grok.context(Interface)
    grok.viewletmanager(IFooter)
    grok.order(3)

    css = "last"

    urlEndings = "kontakt"
    viewURL = "kontakt"
