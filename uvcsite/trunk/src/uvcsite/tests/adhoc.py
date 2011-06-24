# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


import grok
import uvcsite


class Index(uvcsite.Page):
    grok.context(uvcsite.IUVCSite)
    grok.layer(uvcsite.adhoc.IAdHocLayer)
    grok.title('ADHOCSTARTSEITE')
    grok.require('uvc.AdHoc')

    uvcsite.menu(uvcsite.IGlobalMenu)

    def update(self):
        print self.request.principal.groups

    def render(self):
        return "HI Klaus"



