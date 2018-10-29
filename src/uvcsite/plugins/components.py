import grok
import zope.interface
import zope.component
import uvcsite

from zope.location import LocationProxy
from zope.publisher.interfaces import browser
from zope.traversing.interfaces import ITraversable
from zope.dublincore.interfaces import IDCDescriptiveProperties


def unavailable_method(meth):
    def not_implemented(*args):
        raise NotImplementedError('Unavailable method.')
    not_implemented.available = False
    return not_implemented


def is_available(meth):
    return getattr(meth, 'available', True)


class IPlugin(zope.interface.Interface):

    title = zope.interface.Attribute('Title')
    description = zope.interface.Attribute('Description')
    
    def install(site):
        pass

    def uninstall(site):
        pass

    def refresh(site):
        pass

    def get_status(site=None):
        pass

    def get_documentation(*args):
        pass


@zope.interface.implementer(IDCDescriptiveProperties, IPlugin)
class Plugin(grok.GlobalUtility):
    grok.baseclass()
    grok.provides(IPlugin)

    title = None
    description = u""
    is_installed = False

    def install(self, site):
        pass

    def uninstall(self, site):
        pass

    def refresh(self, site):
        pass

    def get_status(self, site):
        pass

    def get_documentation(self, *args):
        pass


class PluginErrors(Exception):

    def __init__(self, title, *errors):
        Exception.__init__(self, title)
        self.errors = errors
