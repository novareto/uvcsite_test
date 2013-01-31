# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


import pytz
import urllib
import uvcsite
import zope.security

from zope.app.homefolder.interfaces import IHomeFolder
from zope.app.security.interfaces import IUnauthenticatedPrincipal


def getHomeFolder(request):
    principal = request.principal
    if IUnauthenticatedPrincipal.providedBy(principal):
        return
    return IHomeFolder(principal).homeFolder


def getHomeFolderUrl(request, suffix=""):
    url = uvcsite.IGetHomeFolderUrl(request).getURL(type=suffix)
    if url:
        url = urllib.unquote(url)
    return url


def fmtDateTime(object, fmt="%d.%m.%Y %H:%M:%S"):
    tz = pytz.timezone("Europe/Berlin")
    return object.astimezone(tz).strftime(fmt)


def fmtZahl(n):
    if isinstance(n, str) or isinstance(n, int):
        r = []
        for i, c in enumerate(reversed(str(n))):
            if i and (not (i % 3)):
                r.insert(0, '.')
            r.insert(0, c)
        return ''.join(r)
    return n


def getRequest():
    return zope.security.management.getInteraction().participations[0]


def getPrincipal():
    return getRequest().principal
