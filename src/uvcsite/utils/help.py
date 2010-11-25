# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from zope import interface, component, viewlet

grok.templatedir('templates')


class HelpManager(grok.ViewletManager):
    """ ViewletManager für HilfeSeiten
    """
    grok.context(interface.Interface)
    grok.name('uvc.hilfen')


class Help(grok.Viewlet):
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.context(interface.Interface)
    grok.order(9999)

    def render(self):
        helpmanager = component.getMultiAdapter(
            (self.context, self.request, self.view), 
            viewlet.interfaces.IViewletManager,
            name=u'uvc.hilfen')
        helpmanager.update()
        return helpmanager.render()



class HelpPage(grok.Viewlet):
    grok.viewletmanager(HelpManager)
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

