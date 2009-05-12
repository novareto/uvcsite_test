# -*- coding: utf-8 -*-

import grok
from zope.i18n import translate
from z3c.menu.simple.menu import GlobalMenuItem



class MenuItem(grok.Viewlet, GlobalMenuItem):
    grok.baseclass()

    def render(self):
	return self.template()
