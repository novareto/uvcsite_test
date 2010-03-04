# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout
from uvcsite.interfaces import IUVCSite, IGlobalMenu, IDocumentActions
from uvcsite.viewlets.utils import DocumentAction


class Index(megrok.layout.Page):
    grok.context(IUVCSite)
    grok.require('zope.View')


class PdfIcon(DocumentAction):
    grok.name(u'aspdf')
    grok.context(IUVCSite)
    grok.viewletmanager(IDocumentActions)

    image = "pdf.png"
    title = 'aspdf'
    urlEndings = 'aspdf'
    viewURL = 'aspdf'
