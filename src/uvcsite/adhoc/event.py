# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok

from zope.pluggableauth.interfaces import IAuthenticatedPrincipalCreated
from zope.interface import alsoProvides
from interfaces import IAdHocPrincipal, IAdHocUserInfo


@grok.subscribe(IAuthenticatedPrincipalCreated)
def mark_adhocuser(factory):
    principal = factory.principal
    ahui = IAdHocUserInfo(principal)
    if ahui.isAdHocUser:
        alsoProvides(principal, IAdHocPrincipal)
        principal.groups.append('uvc.AdHocGroup')
