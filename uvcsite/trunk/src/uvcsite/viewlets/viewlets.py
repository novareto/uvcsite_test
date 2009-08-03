# -*- coding: utf-8 -*-

import grok

from uvcsite.interfaces import IUVCSite
from zope.interface import Interface
from zope.component import getUtility
from zope.traversing.browser import absoluteURL
from uvcsite.interfaces import ILogo, IStatusMessage, IHeaders
from z3c.flashmessage.interfaces import IMessageReceiver

class Favicon(grok.Viewlet):
    """ The Favicon.ico Image"""
    grok.name('favicon')
    grok.context(IUVCSite)
    grok.viewletmanager(IHeaders)

    def update(self):
	import pdb; pdb.set_trace() 

class Image(grok.Viewlet):
    """ Image Things"""
    grok.name('image')
    grok.context(Interface)
    grok.viewletmanager(ILogo)

    def app_url(self):
	#try: 
	#    self.view.application_url()
	#except:
	#    return absoluteURL(self.view, self.view.request)
	return self.view.application_url()


class StatusMessages(grok.Viewlet):
    grok.name('uvcsite.messages')
    grok.context(Interface)
    grok.viewletmanager(IStatusMessage)

    def update(self):
        source = getUtility(IMessageReceiver)
        self.messages = list(source.receive()) 	
