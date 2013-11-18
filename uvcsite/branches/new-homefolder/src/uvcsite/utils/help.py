# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from megrok.pagetemplate import PageTemplate
from zope import interface, component
from zope.viewlet.interfaces import IViewletManager
from zope.pagetemplate.interfaces import IPageTemplate

grok.templatedir('templates')


class HelpManager(grok.ViewletManager):
    """ ViewletManager für HilfeSeiten
    """
    grok.context(interface.Interface)
    grok.name('uvc.hilfen')

    def getHelpPages(self):
        rc = []
        for viewlet in self.viewlets:
            if IHelpPage.providedBy(viewlet):
                rc.append(viewlet)
        return rc 

    def getViewlets(self):
        rc = []
        for viewlet in self.viewlets:
            if not IHelpPage.providedBy(viewlet):
                rc.append(viewlet)
        return rc 

    def render(self):
        template = component.getMultiAdapter((self, self.request), IPageTemplate)
        return template()


class HelpManagerTemplate(PageTemplate):
    grok.view(HelpManager)


class Help(grok.Viewlet):
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.context(interface.Interface)
    grok.order(9999)

    def render(self):
        helpmanager = component.getMultiAdapter(
            (self.context, self.request, self.view), IViewletManager,
            name=u'uvc.hilfen')
        helpmanager.update()
        return helpmanager.render()



class IHelpPage(interface.Interface):
    """ """

class HelpPage(grok.Viewlet):
    grok.viewletmanager(HelpManager)
    grok.implements(IHelpPage)
    grok.baseclass()

    def update(self):
        self.response = self.request.response

    def namespace(self):
        return {'settings_overrides': {'input_encoding': 'utf-8',
                                       'output_encoding': 'unicode',
                                       'stylesheet': '',
                                       'stylesheet_path': None,
                                       'embed_stylesheet' :0,
                }}

