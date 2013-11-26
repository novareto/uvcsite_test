# -*- coding: utf-8 -*-

import uvcsite
import zope.generations.utility


def evolve(context):
    # This depends on zope.app.publication.
    root = zope.generations.utility.getRootFolder(context)
    for name, obj in root.item():
        if uvcsite.IUVCSite.providedBy(obj):
            if obj._sm.__class__ != uvcsite.app.LocalSiteManager:
                newsm = uvcsite.app.LocalSiteManager(obj, default_folder=False)
                newsm.addSub(obj._sm)
                obj._sm = newsm
                print "Migrated the SiteManager on %s" % name
