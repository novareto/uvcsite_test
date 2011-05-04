# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvc.layout.interfaces import IHeaders

grok.templatedir('templates')

class IEFixes(grok.Viewlet):
    grok.context(uvcsite.IMyHomeFolder)
    grok.viewletmanager(IHeaders)
