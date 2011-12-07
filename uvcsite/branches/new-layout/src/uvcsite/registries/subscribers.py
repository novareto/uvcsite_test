# -*- coding: utf-8 -*-

import grokcore.component
from grokcore.site.components import Site
from grok.interfaces import IApplicationInitializedEvent
from zope.component.interfaces import IComponents
from zope.component import queryUtility


def check_and_enforce_new_registries(site):
    new_registry = queryUtility(IComponents, site.__name__)
    if new_registry is not None:
        sm = site.getSiteManager()
        if not new_registry in sm.__bases__:
            # the registry is not yet here.
            # we ought to add it
            sm.addSub(new_registry)
            print "We added %r as a registry base" % new_registry
        else:
            "%r is already a base" % new_registry
    else:
        print "No existing new registries to push in"


@grokcore.component.subscribe(Site, IApplicationInitializedEvent)
def insert_new_registries(site, event):
    check_and_enforce_new_registries(site)

