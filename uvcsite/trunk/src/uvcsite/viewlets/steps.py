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
    grok.order(10000)

    current = "current"
    past = "past"
    future = "future"

    def update(self):
        self.steps = []
        current = self.view.step
        subforms = self.view._getAvailableSubForms()
        self.title = "Fortschrittsanzeige: %s von %s" %(current+1, len(subforms))
        for i, step in enumerate(subforms):
            link = ''
            if i == current:
                css = self.current
                self.title = "%s - %s  +" %(self.title, step.label)
            elif i > current:
                css = self.future
            elif i < current:
                css = self.past
                link= "%s/edit?jump_step=%s" % (self.view.url(), i)
            self.steps.append(
                dict(description = step.label, css=css, link = link)
                )
