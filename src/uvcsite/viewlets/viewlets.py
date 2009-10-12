# -*- coding: utf-8 -*-


import grok

from uvcsite.interfaces import IUVCSite
from zope.interface import Interface
from zope.component import getUtility, getMultiAdapter
from zope.traversing.browser import absoluteURL
from uvcsite.interfaces import ILogo, IStatusMessage, IHeaders, IBreadCrumb
from z3c.flashmessage.interfaces import IMessageReceiver
from z3c.breadcrumb.interfaces import IBreadcrumb, IBreadcrumbs
from uvcsite import uvcsiteMF as _

class Breadcrumb(grok.Viewlet):
    grok.name('breadcrumb')
    grok.context(Interface)
    grok.viewletmanager(IBreadCrumb)

    def render(self):
        bcs = []
        for bc in getMultiAdapter((self.context, self.request),
                                   IBreadcrumbs).crumbs:
            bcs.append("<a href=%s> %s </a>/" %(bc.get('url'), bc.get('name')))
        return "".join(bcs[1:])


class Favicon(grok.Viewlet):
    """ The Favicon.ico Image"""
    grok.name('favicon')
    grok.context(Interface)
    grok.viewletmanager(IHeaders)
    

class Image(grok.Viewlet):
    """ Image Things"""
    grok.name('image')
    grok.context(Interface)
    grok.viewletmanager(ILogo)

    def app_url(self):
        return self.view.application_url()


class StatusMessages(grok.Viewlet):
    grok.name('uvcsite.messages')
    grok.context(Interface)
    grok.viewletmanager(IStatusMessage)

    def update(self):
        source = getUtility(IMessageReceiver)
        self.messages = list(source.receive())
