# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import uvclight
import transaction
import uvcsite

from cromlech.security import Principal
from grokcore.component import subscribe
from uvc.homefolder import IHomefolder
from uvcsite.content import IProductFolder, IUVCApplication
from uvcsite.content.interfaces import IProductRegistration
from zope.component import getAdapters
from zope.lifecycleevent import IObjectAddedEvent


def createProductFolders(principal=None):
    request = zope.security.management.getInteraction().participations[0]
    if not principal:
       principal = request.principal
    for name, pr in getAdapters((principal, request), IProductRegistration):
        pr.createInProductFolder()


@subscribe(IHomefolder, IObjectAddedEvent)
def handle_homefolder(homefolder, event):
    principal = Principal(homefolder.__name__, homefolder.__name__)
    createProductFolders(principal)
