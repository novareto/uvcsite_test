# -*- coding: utf-8 -*-
import uvcsite
from grokcore.component import adapter, implementer
from uvc.homefolder import IHomefolder
from zope.security.interfaces import IPrincipal


@adapter(IPrincipal)
@implementer(IHomefolder)
def principal_homefolder(principal):
    return uvcsite.getHomeFolder(principal)
