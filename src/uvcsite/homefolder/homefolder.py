# -*- coding: utf-8 -*-

from grokcore.component import adapter, implementer
from uvc.homefolder import IHomefolder, IHomefolders
from zope.component import getUtility
from zope.security.interfaces import IPrincipal


@adapter(IPrincipal)
@implementer(IHomefolder)
def principal_homefolder(principal):
    hfs = getUtility(IHomefolders)
    return hfs.get(principal.id)
