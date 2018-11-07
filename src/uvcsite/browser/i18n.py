import grok
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.interface import implementer
from zope.publisher.interfaces.http import IHTTPRequest


@implementer(IUserPreferredLanguages)
class GermanBrowserLangugage(grok.Adapter):
    grok.context(IHTTPRequest)

    def getPreferredLanguages(self):
        return ['de', 'de-de']
