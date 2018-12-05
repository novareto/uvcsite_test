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
            return uvcsite.plugins.Status(
                state=uvcsite.plugins.States.INSTALLED)
        return uvcsite.plugins.Status(
            state=uvcsite.plugins.States.NOT_INSTALLED)

    @uvcsite.plugins.plugin_action('Documentation')
    def documentation(self, site):
        return uvcsite.plugins.Result(
            value=CATALOG_DOC,
            type=uvcsite.plugins.ResultTypes.PLAIN)

    @uvcsite.plugins.plugin_action(
        'Install', uvcsite.plugins.States.NOT_INSTALLED)
    def install(self, site):
        grok.notify(uvcsite.cataloging.CatalogDeployment(site))
        return uvcsite.plugins.Result(
            value=u'Catalog installed with success',
            type=uvcsite.plugins.ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.plugin_action(
        'Diagnostic', uvcsite.plugins.States.INSTALLED)
    def diagnose(self, site):
        sm = site.getSiteManager()
        catalog = sm.getUtility(ICatalog, name="workflow_catalog")
        return uvcsite.plugins.Result(
            value={
                'Plugin type': u'Catalog',
                'Indexes': ', '.join(list(catalog.keys())),
                'Local name': catalog.__name__,
                'Catalog name': u"workflow_catalog",
                'Number of documents': catalog['state'].documentCount(),
                'Remarks': 'Depends on IntIds.'
            },
            type=uvcsite.plugins.ResultTypes.JSON)

    @uvcsite.plugins.plugin_action(
        'Recatalog', uvcsite.plugins.States.INSTALLED)
    def recatalog(self, site):
        sm = site.getSiteManager()
        catalog = sm.getUtility(ICatalog, name="workflow_catalog")
        ids = sm.getUtility(IIntIds)

        counter = 0
        for obj in getContentInAllFolders(site['members']):
            id = ids.queryId(obj)
            if id is not None:
                catalog.index_doc(id, obj)
                counter += 1

        return uvcsite.plugins.Result(
            value=u'%s items recataloged !' % counter,
            type=uvcsite.plugins.ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.plugin_action(
        'Uninstall', uvcsite.plugins.States.INSTALLED)
    def uninstall(self, site):
        sm = site.getSiteManager()
        catalog = sm.queryUtility(ICatalog, name="workflow_catalog")
        if catalog is not None:
            name_in_container = catalog.__name__
            if sm.unregisterUtility(
                    catalog, provided=ICatalog, name="workflow_catalog"):
                del sm[name_in_container]
                return uvcsite.plugins.Result(
                    value=u'Catalog uninstalled with success',
                    type=uvcsite.plugins.ResultTypes.MESSAGE,
                    redirect=True)
            raise uvcsite.plugins.PluginError(
                'Installation error'
                u'Catalog unregistration was unsuccessful.')
        raise uvcsite.plugins.PluginError(
                'Installation error'
                u'Catalog does not exist.')
