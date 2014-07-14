# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import uvclight
from uvc.layout.interfaces import IExtraInfo
from zope import interface


class ExtraInfo(uvclight.ViewletManager):
    uvclight.implements(IExtraInfo)
    uvclight.name('uvc.layout.extrainfo')
    uvclight.context(interface.Interface)
