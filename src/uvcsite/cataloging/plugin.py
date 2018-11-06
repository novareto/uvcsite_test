# -*- coding: utf-8 -*-

import grok
import uvcsite.cataloging
import uvcsite.plugins
from uvcsite.utils.script_helpers import getContentInAllFolders
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds
from zope.lifecycleevent import ObjectModifiedEvent


CATALOG_DOC = u"""Write me

This is a documentation about...
"""


class CatalogPlugin(uvcsite.plugins.Plugin):
    grok.name('uvcsite.catalog')

    fa_icon = 'book'
    title = u"Generic catalog"
    description=(
        u"Cataloging capabilities for searching "
        + u"and sorting items efficiently")

    @property
    def status(self):
        catalog = queryUtility(ICatalog, name="workflow_catalog")
        if catalog is not None:
            return uvcsite.plugins.INSTALLED
        return uvcsite.plugins.NOT_INSTALLED

    @uvcsite.plugins.plugin_action(
        'Documentation', _for=uvcsite.plugins.ANY)
    def documentation(site):
        return uvcsite.plugins.PluginResult(
            value=CATALOG_DOC,
            type=uvcsite.plugins.RAW,
            redirect=False)

    @uvcsite.plugins.plugin_action(
        'Install', _for=uvcsite.plugins.NOT_INSTALLED)
    def install(site):
        grok.notify(uvcsite.cataloging.CatalogDeployment(site))
        return uvcsite.plugins.PluginResult(
            value=u'Catalog installed with success',
            type=uvcsite.plugins.STATUS_MESSAGE,
            redirect=True)

    @uvcsite.plugins.plugin_action(
        'Diagnostic', _for=uvcsite.plugins.INSTALLED)
    def diagnose(site):
        sm = site.getSiteManager()
        catalog = sm.getUtility(ICatalog, name="workflow_catalog")
        return uvcsite.plugins.PluginResult(
            value={
                'Plugin type': u'Catalog',
                'Indexes': ', '.join(list(catalog.keys())),
                'Local name': catalog.__name__,
                'Catalog name': u"workflow_catalog",
                'Number of documents': catalog['state'].documentCount(),
                'Remarks': 'Depends on IntIds.'
            },
            type=uvcsite.plugins.STRUCTURE,
            redirect=False)

    @uvcsite.plugins.plugin_action(
        'Recatalog', _for=uvcsite.plugins.INSTALLED)
    def recatalog(site):
        sm = site.getSiteManager()
        catalog = sm.getUtility(ICatalog, name="workflow_catalog")
        ids = sm.getUtility(IIntIds)

        counter = 0
        for obj in getContentInAllFolders(site['members']):
            id = ids.queryId(obj)
            if id is not None:
                catalog.index_doc(id, obj)
                counter += 1

        return uvcsite.plugins.PluginResult(
            value=u'%s items recataloged !' % counter,
            type=uvcsite.plugins.STATUS_MESSAGE,
            redirect=True)

    @uvcsite.plugins.plugin_action(
        'Uninstall', _for=uvcsite.plugins.INSTALLED)
    def uninstall(site):
        sm = site.getSiteManager()
        catalog = sm.queryUtility(ICatalog, name="workflow_catalog")
        if catalog is not None:
            name_in_container = catalog.__name__
            if sm.unregisterUtility(
                    catalog, provided=ICatalog, name="workflow_catalog"):
                del sm[name_in_container]
                return uvcsite.plugins.PluginResult(
                    value=u'Catalog uninstalled with success',
                    type=uvcsite.plugins.STATUS_MESSAGE,
                    redirect=True)
            raise uvcsite.plugins.PluginErrors(
                'Installation error'
                u'Catalog unregistration was unsuccessful.')
        raise uvcsite.plugins.PluginErrors(
                'Installation error'
                u'Catalog does not exist.')
