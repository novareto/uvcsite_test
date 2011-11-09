# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from uvcsite.adhoc.interfaces import IAdHocFolder
from uvcsite.content import IContent, IProductFolder

class AdHocFolder(grok.Container):
    grok.implements(IAdHocFolder)
