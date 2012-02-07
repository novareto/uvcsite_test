# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import pytz
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


def fmtDateTime(object, fmt="%d.%m.%Y %H:%M:%S"):
    tz = pytz.timezone("Europe/Berlin")
    return object.astimezone(tz).strftime(fmt)
