# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from zope import interface

grok.templatedir('templates')


class HelpManager(grok.ViewletManager):
    """ ViewletManager für HilfeSeiten
    """
    grok.context(interface.Interface)
    grok.name('uvc.hilfen')


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

