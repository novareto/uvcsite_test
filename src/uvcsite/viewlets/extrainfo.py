# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
from zope.interface import Interface, implementer


@implementer(uvcsite.IExtraInfo)
class ExtraInfo(grok.ViewletManager):
    grok.name('uvc.layout.extrainfo')
    grok.context(Interface)
