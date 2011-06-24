# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
from zope.security.interfaces import IPrincipal
from interfaces import IAdHocUserInfo



class AdHocUserInfo(grok.Adapter):
    grok.implements(IAdHocUserInfo)
    grok.context(IPrincipal)

    @property
    def isAdHocUser(self):
        if self.context.title.startswith('A'):
            return True
        return False
