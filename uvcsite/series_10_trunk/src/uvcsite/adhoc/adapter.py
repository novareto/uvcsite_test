# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
from zope.security.interfaces import IPrincipal
from interfaces import IAdHocUserInfo

from uvcsite.auth.interfaces import IMasterUser
from uvcsite.adhoc.interfaces import IAdHocPrincipal
from zope.pluggableauth.factories import Principal


class AdHocUserInfo(grok.Adapter):
    grok.implements(IAdHocUserInfo)
    grok.context(IPrincipal)
    grok.baseclass()

    @property
    def isAdHocUser(self):
        if self.context.title.startswith('A'):
            return True
        return False

    @property
    def addurl(self):
        raise NotImplementedError(
            "concrete classes must implement property info")

    @property
    def info(self):
        raise NotImplementedError(
            "concrete classes must implement property info")

    @property
    def defaults(self):
        raise NotImplementedError(
            "concrete classes must implement property defaults")



@grok.adapter(IAdHocPrincipal)
@grok.implementer(IMasterUser)
def masteruser(self):
    """Return always the Master User"""
    master_id = self.title
    return Principal(master_id)
