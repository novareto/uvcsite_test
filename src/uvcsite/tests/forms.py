# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope import interface
from zope import schema

from dolmen.forms import base
from zeam.form.base import action, DictDataManager 

from uvc.widgets import DatePicker, DatePickerCSS, double
from zeam.form import composed

from uvc.widgets.fields import OptionalChoice


class IPerson(interface.Interface):

    id = schema.TextLine(
       title = u"Id",
       description = u"Id",
       )

    name = schema.TextLine(
       title = u"Name",
       description = u"Bitte geben Sie hier den Namen ein",
       )

    vorname = schema.TextLine(
        title = u"Vorname",
        description = u"Bitte geben Sie den Vornamen ein",
        )

    geschlecht = OptionalChoice(
        title = u"Gender",
        description = u"Bitte geben Sie das Geschlecht ein",
        values = ('men', 'woman', 'kid', 'grandpa', 'sister', 'brother'),
        )

    datum = schema.Date(
        title = u"Datum",
        description = u"Bitte wählen Sie ein Datum aus",
        )


class FormBeispiele(uvcsite.Category):
    grok.title('FormBeispiele')
    grok.context(interface.Interface)
    uvcsite.topmenu(uvcsite.IGlobalMenu)


class MyForm(uvcsite.Form):
    grok.title(u'Beispielform')
    grok.description(u"Beschreibugn Beschreibugn")
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(FormBeispiele)

    ignoreContent = False 
    ignoreRequest = False
    fields = base.Fields(IPerson)

    label = u"Beispielform"
    description = u"Beschreibung"

    def updateWidgets(self):
        super(MyForm, self).updateWidgets()
        self.fieldWidgets.get('form.field.datum').htmlId = lambda x='datepicker': x 

    def update(self):
        self.setContentData(DictDataManager(dict(name="Klaus")))
        double.need()
        DatePicker.need()
        DatePickerCSS.need()

    @action(u'Abschicken')
    def handleButton(self):
       data, errors = self.extractData()
       if errors:
           self.flash(u"FEHLER", type="error")
           return
       self.flash('Alles Klar')
       return 

#
## GroupForm
#

class SplitContact(uvcsite.GroupForm):
    grok.title(u'FieldsetBasedForm')
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(FormBeispiele)


class Father(uvcsite.SubForm):
    composed.context(uvcsite.IUVCSite)
    composed.view(SplitContact)
    fields = base.Fields(IPerson)

    label = "Father"

    @action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()


class Mother(uvcsite.SubForm):
    composed.context(uvcsite.IUVCSite)
    composed.view(SplitContact)
    fields = base.Fields(IPerson)

    label = "Mother"

    @action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()

#
## Wizard
#

class MyWizard(uvcsite.Wizard):
    grok.title('Wizard')
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(FormBeispiele)


class Step1(uvcsite.Step):
    grok.title('Step1')
    grok.context(uvcsite.IUVCSite)
    composed.view(MyWizard)
    fields = base.Fields(IPerson)

    label = "Step 1"



class Step2(uvcsite.Step):
    grok.title('Step2')
    grok.context(uvcsite.IUVCSite)
    composed.view(MyWizard)
    fields = base.Fields(IPerson)

    label = "Step 2"
