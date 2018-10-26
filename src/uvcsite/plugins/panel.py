import grok
import zope.interface
import zope.component
import uvcsite

from zope.location import LocationProxy
from zope.publisher.interfaces import browser
from zope.traversing.interfaces import ITraversable


grok.templatedir('templates')


class IPlugin(zope.interface.Interface):

    title = zope.interface.Attribute('Title')
    
    def install(site):
        pass

    def uninstall(site):
        pass

    def refresh(site):
        pass


@zope.interface.implementer(IPlugin)
class Plugin(grok.GlobalUtility):
    grok.baseclass()

    title = None
    is_installed = False

    def install(site):
        pass

    def uninstall(site):
        pass

    def refresh(site):
        pass
    

class SitePlugin:

    def __init__(self, site, plugin, name=None):
        self.plugin = plugin
        self.site = site
        if name is None:
            name = grok.name.bind().get(plugin)
        self.name = name

    def install(self):
        self.plugin.install(self.site)

    def uninstall(self):
        self.plugin.uninstall(self.site)

    def refresh(self):
        self.plugin.refresh(self.site)

    @property
    def is_installed(self):
        return self.plugin.is_installed


class PluginsPanel:

    def __init__(self, site=None):
        self.site = site or zope.component.hooks.getSite()

    def __iter__(self):
        plugins = zope.component.queryUtilitesFor(IPlugin)
        for name, plugin in plugins:
            yield name, plugin
        
    def __getitem__(self, name):
        plugin = zope.component.queryUtility(IPlugin, name=name)
        if plugin is not None:
            return SitePlugin(self.site, plugin)
        return None


class PluginsNS(grok.MultiAdapter):
    grok.name('plugins')
    grok.provides(ITraversable)
    grok.adapts(uvcsite.IUVCSite, browser.IBrowserRequest)

    def __init__(self, context, request):
        self.panel = LocationProxy(
            PluginsPanel(context), context, '++plugins++')

    def traverse(self, name, ignore):
        if not name:
            return self.panel
        else:
            plugin = self.panel[name]
            if plugin is not None:
                return LocationProxy(plugin, self.panel, "++plugins++" + name)
        return None


class PluginsPanelManagement(uvcsite.Page):
    grok.context(PluginsPanel)
    grok.name('index.html')

    def plugins(self):
        url = self.url(self.context)
        for name, plugin in self.context:
            yield {
                'title': plugin.title,
                'plugin': plugin,
                'url': '%s/%s' % (url, name)
                }
            
    
class PluginOverview(uvcsite.Page):
    grok.context(SitePlugin)
    grok.name('index.html')
