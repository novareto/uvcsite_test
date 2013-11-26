# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import uvcsite
import zope.generations.utility
from uvc.homefolder import IHomefolders


def evolve(context):
    """ MIGRATION OF HOMEFOLDERS"""
    root = zope.generations.utility.getRootFolder(context)
    for name, obj in root.items():
        if uvcsite.IUVCSite.providedBy(obj):

            # migration of member area
            hf = obj['members']
            if hasattr(hf, '_data') is False:
                hf._data = hf._SampleContainer__data
                del hf._SampleContainer__data
                print "migrated Homefolders structure in %s" % name

            for user in obj['members'].values():
                if hasattr(user, '_data') is False:
                    user._data = user._SampleContainer__data
                    del user._SampleContainer__data
                    print "migrated user %s in %s" % (user.__name__, name)

            # Add membership to sm
            if obj._sm.queryUtility(IHomefolders) is None:
                members = obj['members']
                obj._sm.registerUtility(members, IHomefolders)
                print "Added IHomefolders in %s" % name
