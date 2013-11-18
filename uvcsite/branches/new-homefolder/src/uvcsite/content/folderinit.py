# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
from uvc.homefolder.interfaces import IHomefolder
from uvcsite.content.interfaces import IProductRegistration
from zope.component import getAdapters
from zope.pluggableauth.factories import Principal
from zope.security.management import getInteraction


def createProductFolders(principal=None):
    request = getInteraction().participations[0]
    if not principal:
       principal = request.principal
    for name, pr in getAdapters((principal, request), IProductRegistration):
        pr.createInProductFolder()


@grok.subscribe(IHomefolder, grok.IObjectAddedEvent)
def handle_homefolder(homefolder, event):
    principal = Principal(homefolder.__name__, homefolder.__name__)
    createProductFolders(principal)
