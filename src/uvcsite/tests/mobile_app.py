# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite


class OverView(uvcsite.MobilePage):
    grok.name('index')
    grok.context(uvcsite.IUVCSite)
    grok.order(10)
    grok.require('zope.View')

    def update(self):
        print self.request.principal

    def render(self):
        return '''<div data-role="content">
                  <p> HALLO NASE </p> 
                  <p>Seite2 <a href="#page2"> Seite2 </a> 
                  <p>URL-Schemas <a href="#urlschemas"> URL-Schemas </a> 
                  <a href="#confirmation" data-rel="dialog" data-transition="pop"> Lschen </a>
                  </div> '''

