import sys
import grok
import zope.interface
import zope.component

from collections import namedtuple
from functools import wraps

from zeam.form.base import Actions, Action, FAILURE
from zope.location import LocationProxy
from zope.publisher.interfaces import browser
from zope.traversing.interfaces import ITraversable
from zope.dublincore.interfaces import IDCDescriptiveProperties

import uvcsite.plugins
from uvcsite.plugins import flags


PluginResult = namedtuple(
    'PluginResult', ['value', 'type', 'redirect'])


class IPlugin(zope.interface.Interface):

    title = zope.interface.Attribute('Title')
    description = zope.interface.Attribute('Description')
    actions = zope.interface.Attribute('Actions')
    status = zope.interface.Attribute('Plugin status')


class PluginAction(Action):

    prefix = "plugin"

    def __init__(self, callback, _for, title=None):
        self._for = _for
        self.callback = callback
        Action.__init__(
            self, title=title, identifier=callback.__name__)

    def available(self, form):
        plugin = form.getContent()
        if isinstance(self._for, (list, tuple, set)):
            return plugin.status in self._for
        return self._for == plugin.status

    def __call__(self, form):
        site = grok.getApplication()
        try:
            result = self.callback(site)
            assert isinstance(result, PluginResult)
            return result
        except PluginErrors as exc:
            form.errors = Errors(*[
                Error(title=error, identifier=self.identifier)
                for error in exc.errors])
        return FAILURE


def plugin_action(title, _for=flags.ANY):
    def callback(method):
        frame = sys._getframe(1)
        f_locals = frame.f_locals
        actions = f_locals.setdefault('actions', Actions())
        action = PluginAction(method, title=title, _for=_for)
        actions.append(action)
        return method
    return callback

    
@zope.interface.implementer(IDCDescriptiveProperties, IPlugin)
class Plugin(grok.GlobalUtility):
    grok.baseclass()
    grok.provides(IPlugin)

    title = None
    description = u""
    status = flags.UNINSTALLED
    actions = None


class PluginErrors(Exception):

    def __init__(self, title, *errors):
        Exception.__init__(self, title)
        self.errors = errors
