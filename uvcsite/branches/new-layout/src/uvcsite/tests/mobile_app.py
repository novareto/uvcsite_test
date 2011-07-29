# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite





class OverView(uvcsite.MobilePage):
    grok.name('index')
    grok.context(uvcsite.IUVCSite)
    grok.order(10)

    def render(self):
        return '<div data-role="content"><h1> HALLO NASE <h1></div> '
