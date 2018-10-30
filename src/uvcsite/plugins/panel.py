# -*- coding: utf-8 -*-

import grok
import zope.interface
import zope.component
import uvcsite

from zeam.form.base import Errors, Error
from zope.location import Location, LocationProxy
from zope.publisher.interfaces import browser
from zope.container.interfaces import IReadContainer
from zope.traversing.interfaces import ITraversable
from zope.dublincore.interfaces import IDCDescriptiveProperties

from uvcsite.plugins import INSTALLED, STATUS_MESSAGE, RAW, STRUCTURE
from uvcsite.plugins.components import PluginErrors, IPlugin


grok.templatedir('templates')


@zope.interface.implementer(IReadContainer, IDCDescriptiveProperties)
class PluginsPanel(Location):

    title = u"Plugins management panel"
    description = (u"Application panel listing all the plugins "
                   + u"manageable via the interface")

    def __init__(self, name, parent):
        self.__name__ = name
        self.__parent__ = parent

    def __iter__(self):
        plugins = zope.component.getUtilitiesFor(IPlugin)
        for name, plugin in plugins:
            yield name, LocationProxy(plugin, self, name)

    def __getitem__(self, name):
        plugin = zope.component.getUtility(IPlugin, name=name)
        return LocationProxy(plugin, self, name)

    def __contains__(self, name):
        return zope.component.queryUtility(IPlugin, name=name) is not None

    def get(self, name):
        plugin = zope.component.queryUtility(IPlugin, name=name)
        if plugin is not None:
            return LocationProxy(plugin, self, name)
        return None


class PluginsPanelManagement(uvcsite.Page):
    grok.context(PluginsPanel)
    grok.name('index.html')

    needs_fontawesome = True
    
    def plugins(self):
        url = self.url(self.context)
        for name, plugin in self.context:
            yield {
                'id': name,
                'title': plugin.title,
                'plugin': plugin,
                'icon': 'fas fa5x fa-' + getattr(plugin, 'fa_icon', 'wrench'),
                'url': '%s/%s' % (url, name)
                }


class PluginOverview(uvcsite.Form):
    grok.context(IPlugin)
    grok.name('index.html')

    prefix = ""
    fields = uvcsite.Fields()
    needs_fontawesome = True

    @property
    def actions(self):
        return self.getContent().actions
        
    def updateForm(self):
        form, action, result = self.updateActions()
        if action is not None:
            self.title = action.title
            if result.type is STATUS_MESSAGE:
                self.flash(result.value)
                if result.redirect:
                    return self.redirect(self.url(self.context))
            elif result.type is RAW:
                self.result = result.value
                self.content_type = 'text'
            elif result.type is STRUCTURE:
                self.result = result.value
                self.content_type = 'struct'

        self.updateWidgets()

    def update(self):
        self.title = None
        self.result = None
        self.content_type = None
        self.is_installed = self.context.status == INSTALLED
