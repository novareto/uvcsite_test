# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import z3c.flashmessage.interfaces
import megrok.pagetemplate as pt

from grok import util
from zope import component

from zeam.form import base
from zeam.form import layout
from dolmen.forms.base import ApplicationForm, apply_data_event
from zeam.form.base.interfaces import ICollection 

import zope.event
import zope.lifecycleevent

from zeam.form.composed import SubForm as BaseSubForm
from zeam.form.composed import ComposedForm
from zope.schema.interfaces import IField

from dolmen.forms import wizard

grok.templatedir('templates')

class Form(ApplicationForm):
    """ Base Class form ZEAM-FORM"""
    grok.baseclass()

    @property
    def formErrors(self):
        error = self.errors.get(self.prefix, None)
        if error is None or ICollection.providedBy(error):
            return error
        return [error]


class GroupForm(ComposedForm, Form):
    grok.baseclass()


class Wizard(wizard.Wizard, Form):
    grok.baseclass()

    def validateData(self, fields, data):
        fields = [x for x in fields if IField.providedBy(x)]
        if not fields:
            return super(ApplicationForm, self).validateData(fields, data)
        return super(wizard.Wizard, self).validate(fields, data)


class Step(wizard.WizardStep, Form):
    grok.baseclass()


class AddForm(Form):
    grok.baseclass()
    _finishedAdd = False 

    @base.action(u'Hinzufügen')
    def handleAdd(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten')
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True

    def createAndAdd(self, data):
        obj = self.create(data)
        zope.event.notify(zope.lifecycleevent.ObjectCreatedEvent(obj))
        self.add(obj)
        return obj

    def create(self, data):
        raise NotImplementedError

    def add(self, object):
        raise NotImplementedError

    def nextURL(self):
        raise NotImplementedError

    def render(self):
        if self._finishedAdd:
            self.request.response.redirect(self.nextURL())
            return ""
        return super(AddForm, self).render()


class SubForm(BaseSubForm):
    grok.baseclass()


class FormTemplate(pt.PageTemplate):
    """Template for a layout aware form.
    """
    pt.view(Form)


class AddFormTemplate(pt.PageTemplate):
    """Template for a layout aware form.
    """
    template = grok.PageTemplateFile('templates/formtemplate.pt')
    pt.view(AddForm)


class SubFormTemplate(pt.PageTemplate):
    """Template for a layout aware form.
    """
    template = grok.PageTemplateFile('templates/formtemplate.pt')
    pt.view(SubForm)


class WizardTemplate(pt.PageTemplate):
    """Template for a layout aware form.
    """
    template = grok.PageTemplateFile('templates/wizardtemplate.pt')
    pt.view(Wizard)
