# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope import interface
from zope import schema

from uvc.widgets import DatePicker, DatePickerCSS, double
from uvc.widgets.fields import OptionalChoice


class IPerson(interface.Interface):

    id = schema.TextLine(
       title = u"Id",
       description = u"Id",
       max_length=3,
       )

    name = schema.TextLine(
       title = u"Name",
       description = u"Bitte geben Sie hier den Namen ein",
       )

    vorname = schema.TextLine(
        title = u"Vorname",
        description = u"Bitte geben Sie den Vornamen ein",
        )

    geschlecht = schema.Choice(
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
    fields = uvcsite.Fields(IPerson)
    #fields['geschlecht'].mode = "radio"

    label = u"Beispielform"
    description = u"Beschreibung"

    def updateWidgets(self):
        super(MyForm, self).updateWidgets()
        self.fieldWidgets.get('form.field.datum').htmlId = lambda x='datepicker': x 

    def update(self):
        self.setContentData(uvcsite.DictDataManager(dict(name="Klaus")))
        double.need()
        DatePicker.need()
        DatePickerCSS.need()

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
       data, errors = self.extractData()
       if data.get('name') == "hans":
           self.errors.append(uvcsite.Error('Hans ist doof', identifier=self.prefix))
       if errors or self.errors:
           self.flash(u"FEHLER", type="error")
           return
       self.flash('Alles Klar')
       return 



class MyFormHilfe(uvcsite.HelpPage):
    grok.context(uvcsite.IUVCSite)
    grok.view(MyForm)


#
## GroupForm
#

class SplitContact(uvcsite.GroupForm):
    grok.title(u'FieldsetBasedForm')
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(FormBeispiele)


class Father(uvcsite.SubForm):
    grok.context(uvcsite.IUVCSite)
    grok.view(SplitContact)
    fields = uvcsite.Fields(IPerson)

    label = "Father"

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()


class Mother(uvcsite.SubForm):
    grok.context(uvcsite.IUVCSite)
    grok.view(SplitContact)
    fields = uvcsite.Fields(IPerson)

    label = "Mother"

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()

#
## Wizard
#

class MyWizard(uvcsite.Wizard):
    grok.title('Wizard')
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(FormBeispiele)
    label = u"Wizard"
    description = u"Ein Beispiel WIZARD"

    def __init__(self, context, request):
        super(MyWizard, self).__init__(context, request)
        #self.setContentData(DictDataManager({}))


class Step1(uvcsite.Step):
    grok.title('Step1')
    grok.context(uvcsite.IUVCSite)
    grok.view(MyWizard)
    fields = uvcsite.Fields(IPerson).select('datum')
    ignoreContent = False

    label = "Step 1"


class Step2(uvcsite.Step):
    grok.title('Step2')
    grok.context(uvcsite.IUVCSite)
    grok.view(MyWizard)
    fields = uvcsite.Fields(IPerson).select('vorname')
    ignoreContent = False

    label = "Step 2 GANZ LANGER STEP"


class Step3(uvcsite.Step):
    grok.title('Step3')
    grok.context(uvcsite.IUVCSite)
    grok.view(MyWizard)
    fields = uvcsite.Fields(IPerson).select('name')
    ignoreContent = False

    label = "Step 3"


class MyFormHilfe(uvcsite.HelpPage):
    grok.context(uvcsite.IUVCSite)
    grok.view(MyWizard)

