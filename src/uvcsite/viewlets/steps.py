# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite
from zope.interface import Interface


grok.templatedir('templates')


class StepsProgressBar(grok.Viewlet):
    grok.context(Interface)
    grok.view(uvcsite.Wizard)
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.order(10000)
