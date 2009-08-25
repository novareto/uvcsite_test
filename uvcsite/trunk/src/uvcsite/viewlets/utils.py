# -*- coding: utf-8 -*-


import grok
from zope.i18n import translate
from z3c.menu.simple.menu import GlobalMenuItem
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class MenuItem(grok.Viewlet, GlobalMenuItem):
    grok.baseclass()
    template = ViewPageTemplateFile('menu_item.pt')

    def render(self):
        # This method is for grok not to say template or render needed!
        return self.template()
