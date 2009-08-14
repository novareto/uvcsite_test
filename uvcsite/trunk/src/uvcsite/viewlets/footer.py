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

