# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite
from zope import interface

class ExtraInfo(grok.ViewletManager):
    grok.implements(uvcsite.IExtraInfo)
    grok.name('uvc.layout.extrainfo')
    grok.context(interface.Interface)
