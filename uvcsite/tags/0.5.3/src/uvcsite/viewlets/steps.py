# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite
from zope.interface import Interface


grok.templatedir('templates')


class StepsProgressBar(grok.Viewlet):
    grok.context(Interface)
    grok.view(uvcsite.Wizard)
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.order(2000)


    def update(self):
        self.steps = []
        current = self.view.step
        self.title = "Fortschrittsanzeige: %s von %s" %(current+1, len(self.view.subforms))
        for i, step in enumerate(self.view.subforms):
            if i == current:
                css = "current"
                self.title = "%s - %s  +" %(self.title, step.label)
            elif i > current:
                css = "future"
            elif i < current:
                css = "past"
            self.steps.append(
                dict(description = step.label, css=css,)
                )
