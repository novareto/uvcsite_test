# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de 

import grok
import megrok.menu 
from zope.interface import Interface
from uvcsite.interfaces import IDocumentActions
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.publisher.interfaces.browser import IBrowserMenu
from zope.component import getUtility

# Viewlet Implmentation

class DocumentActionsViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IDocumentActions)
    grok.PageTemplateFile('actions_templates/documentactionsviewlet.pt')

    entry_class = u"entry"
    actions = []
