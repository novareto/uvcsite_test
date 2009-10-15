# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de 

import grok

from megrok.layout import Page as base_Page
from megrok.z3ctable import TablePage as base_TablePage

from zope.component import getUtility
from z3c.flashmessage.interfaces import IMessageSource
from uvcsite.content import IUVCApplication

class ApplicationAwareView(object):
    """A mixin allowing to access the application url"""

    def application_url(self, name=None):
        """Return the URL of the nearest Dolmen site.
        """
        obj = self.context
        while obj is not None:
            if IUVCApplication.providedBy(obj):
                return self.url(obj, name)
            obj = obj.__parent__
        print self.context
        raise ValueError("No application found.")

    def flash(self, message, type='message'):
        """Send a short message to the user.
        """
        source = getUtility(IMessageSource, name='session')
        source.send(message, type)


class TablePage(base_TablePage, ApplicationAwareView):
    grok.baseclass()

class Page(base_Page, ApplicationAwareView):
    grok.baseclass()
