# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import transaction
import uvcsite

from uvc.homefolder.interfaces import IHomefolder, IHomefolders
from uvcsite.content import IProductFolder, IUVCApplication
from uvcsite.content.interfaces import IProductRegistration
from zope.component import getAdapters
from zope.pluggableauth.factories import Principal


def createProductFolders(principal=None):
    request = zope.security.management.getInteraction().participations[0]
    if not principal:
       principal = request.principal
    for name, pr in getAdapters((principal, request), IProductRegistration):
        pr.createInProductFolder()


@grok.subscribe(IHomefolder, grok.IObjectAddedEvent)
def handle_homefolder(homefolder, event):
    principal = Principal(homefolder.__name__, homefolder.__name__)
    createProductFolders(principal)
