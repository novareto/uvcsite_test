# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import uvcsite

from zope.app.homefolder.interfaces import IHomeFolder
from zope.app.security.interfaces import IUnauthenticatedPrincipal


def getHomeFolder(request):
    principal = request.principal
    if IUnauthenticatedPrincipal.providedBy(principal):
        return
    return IHomeFolder(principal).homeFolder


def getHomeFolderUrl(request, suffix=""):
    return uvcsite.IGetHomeFolderUrl(request).getURL(type=suffix)