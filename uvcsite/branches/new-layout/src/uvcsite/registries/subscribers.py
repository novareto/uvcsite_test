# -*- coding: utf-8 -*-

import grokcore.component
from grokcore.site.components import Site
from grok.interfaces import IApplicationInitializedEvent
from zope.component.interfaces import IComponents
from zope.component import queryUtility
import zope.processlifetime
from zope.app.publication.zopepublication import ZopePublication
from uvcsite.content import IUVCApplication
from zope.app.appsetup.interfaces import IDatabaseOpenedWithRootEvent


def check_and_enforce_new_registries(site):
    new_registry = queryUtility(IComponents, site.__name__)
    if new_registry is not None:
        sm = site.getSiteManager()
        if not new_registry in sm.__bases__:
            # the registry is not yet here.
            # we ought to add it
            sm.__bases__ = (new_registry,) + tuple(sm.__bases__)


@grokcore.component.subscribe(Site, IApplicationInitializedEvent)
def insert_new_registries(site, event):
    check_and_enforce_new_registries(site)


@grokcore.component.subscribe(IDatabaseOpenedWithRootEvent)
def check_for_registries_update(event):
    connection = event.database.open()
    for object in connection.root()[ZopePublication.root_name].values():
        if IUVCApplication.providedBy(object):
             check_and_enforce_new_registries(object)
