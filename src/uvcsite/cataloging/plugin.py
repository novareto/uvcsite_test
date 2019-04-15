# -*- coding: utf-8 -*-

import grok
import uvcsite
import uvcsite.cataloging
import uvcsite.plugins

from collections import defaultdict
from zope.component.hooks import getSite


CATALOG_DOC = u"""Write me

This is a documentation about...
"""


class CatalogPlugin(uvcsite.plugins.Cataloger, uvcsite.plugins.Plugin):
    grok.name('uvcsite.catalog')

    fa_icon = 'book'
    title = u"Generic catalog"
    description=(
        u"Cataloging capabilities for searching "
        + u"and sorting items efficiently")

    def __init__(self):
        self.catalog = uvcsite.cataloging.WorkflowCatalog
        self.trigger = uvcsite.cataloging.CatalogDeployment

    @uvcsite.plugins.plugin_action('Documentation')
    def documentation(self, site):
        return uvcsite.plugins.Result(
            value=CATALOG_DOC,
            type=uvcsite.plugins.ResultTypes.PLAIN)

    @uvcsite.plugins.plugin_action(
        'Install', uvcsite.plugins.States.NOT_INSTALLED)
    def _install(self, site):
        super(CatalogPlugin, self).install(site)
        return uvcsite.plugins.Result(
            value=u'Install was successful.',
            type=uvcsite.plugins.ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.plugin_action(
        'Diagnostic', uvcsite.plugins.States.INSTALLED)
    def _diagnose(self, site):
        diag = super(CatalogPlugin, self).diagnose(site)
        return uvcsite.plugins.Result(
            value=diag,
            type=uvcsite.plugins.ResultTypes.JSON)

    @uvcsite.plugins.plugin_action(
        'Recatalog', uvcsite.plugins.States.INSTALLED)
    def _recatalog(self, site):
        iterator = getContentInAllFolders(site['members'])
        super(CatalogPlugin, self).recatalog(site, iterator)
        return uvcsite.plugins.Result(
            value=u'Recataloging was successful.',
            type=uvcsite.plugins.ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.plugin_action(
        'Uninstall', uvcsite.plugins.States.INSTALLED)
    def _uninstall(self, site):
        super(CatalogPlugin, self).uninstall(site)
        return uvcsite.plugins.Result(
            value=u'Uninstall was successful.',
            type=uvcsite.plugins.ResultTypes.MESSAGE,
            redirect=True)

    @uvcsite.plugins.plugin_action(
        'Count', uvcsite.plugins.States.INSTALLED)
    def count(self, site):
        catalog = self.get(site)
        counted = defaultdict(dict)
        for type, tids in catalog['type']._fwd_index.items():
            for state, sids in catalog['state']._fwd_index.items():
                counted[type][state] = len(set(tids) & set(sids))
        return uvcsite.plugins.Result(
            value=counted,
            type=uvcsite.plugins.ResultTypes.JSON)
