import grok
import uvcsite
import zope.interface


class Favicon(grok.View):
    """ Helper for Favicon.ico Errors Request
    """
    grok.context(zope.interface.Interface)
    grok.name('favicon.ico')
    grok.require('zope.Public')

    def render(self):
        return "BLA"


class HAProxyCheck(grok.View):
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    def render(self):
        return "OK"
