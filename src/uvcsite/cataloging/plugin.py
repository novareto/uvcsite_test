# -*- coding: utf-8 -*-

import grok
import uvcsite.plugins
import uvcsite.cataloging
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility
from zope.intid.interfaces import IIntIds


CATALOG_DOC = u"""Write me

This is a documentation about...
"""


class CatalogPlugin(uvcsite.plugins.Plugin):
    grok.name('uvcsite.catalog')

    title = u"UVCSite catalog"
    description=(
        u"Cataloging capabilities for searching "
        + u"and sorting items efficiently")

    @property
    def is_installed(self):
        catalog = queryUtility(ICatalog, name="workflow_catalog")
        return catalog is not None

    def install(self, site):
        grok.notify(uvcsite.cataloging.CatalogDeployment(site))
        return None

    def uninstall(self, site):
        sm = site.getSiteManager()
        catalog = sm.queryUtility(ICatalog, name="workflow_catalog")
        if catalog is not None:
            name_in_container = catalog.__name__
            if sm.unregisterUtility(
                    catalog, provided=ICatalog, name="workflow_catalog"):
                del sm[name_in_container]
                return True
            raise uvcsite.plugins.PluginErrors(
                'Installation error'
                u'Catalog unregistration was unsuccessful.')
        raise uvcsite.plugins.PluginErrors(
                'Installation error'
                u'Catalog does not exist.')

    def get_documentation(self, *args):
        return CATALOG_DOC

    def get_status(self, site):
        sm = site.getSiteManager()
        catalog = sm.getUtility(ICatalog, name="workflow_catalog")
        return {
            'Plugin type': u'Catalog',
            'Indexes': ', '.join(list(catalog.keys())),
            'Local name': catalog.__name__,
            'Catalog name': u"workflow_catalog",
            'Number of documents': catalog['state'].documentCount(),
            'Remarks': 'Depends on IntIds.'
        }

    @uvcsite.plugins.unavailable_method
    def refresh(self, site):
        pass
