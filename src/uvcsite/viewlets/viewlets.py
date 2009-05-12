# -*- coding: utf-8 -*-

import grok

from zope.interface import Interface
from uvcsite.interfaces import ILogo
from zope.traversing.browser import absoluteURL

class Image(grok.Viewlet):
    """ Image Things"""
    grok.name('image')
    grok.context(Interface)
    grok.viewletmanager(ILogo)

    def app_url(self):
	try: 
	    self.view.application_url()
	except:
	    return absoluteURL(self.view, self.view.request)
	return self.view.application_url()
