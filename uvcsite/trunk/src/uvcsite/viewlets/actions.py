# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de 

import grok
import megrok.menu 
from zope.interface import Interface
from uvcsite.interfaces import IDocumentActions
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.app.publisher.interfaces.browser import IBrowserMenu
from uvcsite.app import DocumentActions
from zope.component import getUtility

# Viewlet Implmentation

class DocumentActionsViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IDocumentActions)
    grok.PageTemplateFile('actions_templates/documentactionsviewlet.pt')

    entry_class = u"entry"
    actions = []

    def get_context(self):
        return self.context

    def get_actions(self, context):
        menu = getUtility(IBrowserMenu, 'documentactions')
        actions = menu.getMenuItems(context, self.request)
        return menu.title, actions

    def update(self):
        """Gets the actions and determines which is the selected one.
        """
        context = self.get_context()
        self.title, actions = self.get_actions(context)
        
        if actions:
            url = absoluteURL(context, self.request)
            selected = getattr(self.view, '__name__', None)
            self.actions = [{'url': "%s/%s" % (url, action['action']),
                             'title': action['title'],
                             'icon': action['icon'],
                             'css': (action['action'] == selected
                                     and self.entry_class + ' selected'
                                     or self.entry_class)}
                            for action in actions]
