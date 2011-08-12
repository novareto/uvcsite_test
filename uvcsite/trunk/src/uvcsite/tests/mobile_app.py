# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite


class Index(uvcsite.mobile.BaseMobilePage):
    grok.context(uvcsite.IUVCSite)


class OverView(uvcsite.MobilePage):
    grok.name('index')
    grok.context(uvcsite.IUVCSite)
    grok.order(10)
    grok.require('zope.View')
    grok.view(Index)

    def update(self):
        print self.request.principal

    def render(self):
        return '''<div data-role="content">
                  <p> I am Page 1  </p> 
                  <p> Link to Page2 <a href="#page2"> Page2 </a> 
                  </div> '''


class Page2(uvcsite.MobilePage):
    grok.name('page2')
    grok.context(uvcsite.IUVCSite)
    grok.order(20)
    grok.require('zope.View')
    grok.view(Index)

    def render(self):
        return '''<div data-role="content">
                  <p> Page  </p>
                  </div>'''
