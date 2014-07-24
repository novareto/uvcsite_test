# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

from os import path

import uvclight
import uvcsite

from uvc.design.canvas import IAboveContent
from zope.interface import Interface


from cromlech.browser import IView
class IWizard(IView):
    # temporary, until we have a wizard component
    pass


class StepsProgressBar(uvclight.Viewlet):
    uvclight.context(Interface)
    uvclight.view(IWizard)
    uvclight.viewletmanager(IAboveContent)
    uvclight.order(10000)

    template = uvclight.get_template(
        'stepsprogressbar.cpt', path.dirname(__file__))
    
    current = "current"
    past = "past"
    future = "future"
    
    def update(self):
        self.steps = []
        current = self.view.step
        subforms = self.view._getAvailableSubForms()
        self.title = "Fortschrittsanzeige: %s von %s" % (
            current+1, len(subforms))

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
