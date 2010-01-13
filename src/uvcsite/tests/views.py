# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout

from uvcsite import ApplicationAwareView
from uvcsite.interfaces import IUVCSite, IGlobalMenu


class Index(megrok.layout.Page, ApplicationAwareView):
    grok.context(IUVCSite)
    grok.require('zope.View')


