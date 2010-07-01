# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import zope.interface
import zope.component

import megrok.z3cform.wizard as z3cwizard
from z3c.form.interfaces import IErrorViewSnippet

class BasicStep(z3cwizard.PageStep):
    """ Base Class for a WizardStep of UVCSite
    """

    label = form_name = u""
    grok.baseclass()

    def extractData(self):
        data, errors = z3cwizard.PageStep.extractData(self)
        step_errors = []
        for field, message in self.validateStep(data):
            widget = self.widgets[field]
            error = zope.interface.Invalid(message)
            view = zope.component.getMultiAdapter(
                    (error, self.request, widget, widget.field,
                     self, self.context), IErrorViewSnippet)
            view.update()
            if not widget.error:
                widget.error = view
            step_errors.append(view)
        if step_errors:
            errors += tuple(step_errors)
        return data, errors    

    def validateStep(self, data):
        return []

