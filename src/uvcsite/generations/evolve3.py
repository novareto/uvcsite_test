# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import zope.generations.utility


def evolve(context):
    """ MIGRATION OF HOMEFOLDERS"""
    root = zope.generations.utility.getRootFolder(context)
