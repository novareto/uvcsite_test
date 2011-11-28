# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite


class OverView(uvcsite.MobilePage):
    grok.name('index')
    grok.context(uvcsite.IUVCSite)
    grok.order(10)
    grok.require('zope.Public')


class Index(uvcsite.mobile.BaseMobilePage):
    grok.context(uvcsite.IUVCSite)
    theme = "a"

    def render(self):
        return '''<div data-role="content">
                  <p> HALLO NASE </p> 
                  <p>Seite2 <a href="#page2"> Seite2 </a> 
                  <p>URL-Schemas <a href="#urlschemas"> URL-Schemas </a> 
                  <a href="#confirmation" data-rel="dialog" data-transition="pop"> Lschen </a>
                  </div> '''

class Page2(uvcsite.MobilePage):
    grok.name('page2')
    grok.context(uvcsite.IUVCSite)
    grok.order(20)
    grok.require('zope.Public')

    def render(self):
        return '<div data-role="content"><p> Ich bin Seite 2 </p> <p> zur Seite1 <a href="#index"> Seite1 </a> </div> '


class Confirmation(uvcsite.MobilePage):
    grok.context(uvcsite.IUVCSite)
    grok.order(30)
    grok.require('zope.Public')
    
    def render(self):
        return '<div data-role="content"> <p> Lschen? </p> </div>'

class URLSchemas(uvcsite.MobilePage):
    grok.context(uvcsite.IUVCSite)
    grok.order(40)
    grok.name('urlschemas')
    grok.require('zope.Public')

#
###
#

import uvcsite.mobile

class Delete(uvcsite.mobile.BaseMobilePage):
    grok.name('delete')


class Main(uvcsite.MobilePage):
    grok.context(uvcsite.IUVCSite)
    grok.name('main')
    grok.order(10)
    grok.require('zope.View')
    grok.view(Index)


class ConfBook(uvcsite.MobilePage):
    grok.context(uvcsite.IUVCSite)
    grok.view(Delete)
    grok.name('confbook')
    grok.order(20)

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
