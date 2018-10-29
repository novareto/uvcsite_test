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

from .components import PluginErrors, IPlugin, is_available


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


class PluginAction(uvcsite.Action):

    prefix = "plugin"

    def __init__(self, method, should_be_installed=False,
                 success=u'Done', write_on=None,
                 title=None, identifier=None, **htmlAttributes):

        self.should_be_installed = should_be_installed
        self.method = method
        self.write_on = write_on
        self.success = success
        uvcsite.Action.__init__(
            self, title=title, identifier=method, **htmlAttributes)

    def available(self, form):
        plugin = form.getContent()
        if is_available(getattr(plugin, self.method)):
            return (self.should_be_installed is None or
                    self.should_be_installed == plugin.is_installed)

    def __call__(self, form):
        plugin = form.getContent()
        method = getattr(plugin, self.method)
        site = grok.getApplication()
        try:
            value = method(site)
        except PluginErrors as exc:
            form.errors = Errors(*[
                Error(title=error, identifier=self.method)
                for error in exc.errors])
            return uvcsite.FAILURE
        else:
            if self.write_on:
                setattr(form, self.write_on, value)
            else:
                form.flash(self.success)
                url = form.url(plugin)
                return form.redirect(url)
            return uvcsite.SUCCESS


class PluginOverview(uvcsite.Form):
    grok.context(IPlugin)
    grok.name('index.html')

    prefix = ""

    styles = {
        "plugin.install": (['btn-success'], 'fas fa-cog'),
        "plugin.get_status": (['btn-primary'], 'fas fa-info-circle'),
        "plugin.get_documentation": (['btn-info'], 'fas fa-question'),
        "plugin.refresh": (['btn-warning'], 'fas fa-redo-alt'),
        "plugin.uninstall": (['btn-danger'], 'fas fa-trash-alt')
        }

    fields = uvcsite.Fields()
    actions = uvcsite.Actions(
        PluginAction(
            'get_documentation',
            title="About",
            write_on="about",
            should_be_installed=None,
        ),
        PluginAction(
            'install',
            title="Install",
            success=u"Plugin installed with success."
        ),
        PluginAction(
            'get_status',
            title="Diagnose",
            write_on="status",
            should_be_installed=True,
        ),
        PluginAction(
            'refresh',
            title="Refresh",
            should_be_installed=True,
            success=u"Plugin components are now refresh and up to date."
        ),
        PluginAction(
            'uninstall',
            title="Uninstall",
            should_be_installed=True,
            success=u"This plugin is now uninstalled.",
            **{'class': 'btn btn-danger'}
        )
    )

    needs_fontawesome = True

    def updateForm(self):
        uvcsite.Form.updateForm(self)
        for widget in self.actionWidgets:
            styles = self.styles.get(widget.identifier)
            if styles is not None:
                widget.defaultHtmlClass, widget.icon = styles

    def update(self):
        self.status = None
        self.about = None
