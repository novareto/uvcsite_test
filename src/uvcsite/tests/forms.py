# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope import interface
from zope import schema

from zeam.form.base.widgets import getWidgetExtractor
from uvc.widgets import DatePicker, DatePickerCSS, double, jqt_helper
from uvc.widgets.resources import validation
from uvc.widgets.fields import OptionalChoice
from zope.i18n import translate

from uvc.skin.skin import IUVCSkin

grok.layer(IUVCSkin)

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

    datum1 = schema.Date(
        title = u"Datumiii1",
        description = u"Bitte wählen Sie ein Datum aus",
        )


class FormBeispiele(uvcsite.Category):
    grok.title('FormBeispiele')
    grok.context(interface.Interface)
    uvcsite.topmenu(uvcsite.IGlobalMenu)

from zeam.form.base import Form
from zope import component
from megrok.layout.interfaces import ILayout
from zope.publisher.publish import mapply

class PopUpForm(uvcsite.Form):
    grok.title(u'PopUp Beispielform')
    grok.description('Beschreibung')
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(FormBeispiele)

    ignoreContent = False 
    ignoreRequest = False
    fields = uvcsite.Fields(IPerson)

    label = u"PopUp Form"
    description = u"Beispiel PopUp Form"

    def update(self):
        jqt_helper.need()
        DatePicker.need()
        DatePickerCSS.need()

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        print data, errors
        return "HALLO"


    def __call__(self):
        mapply(self.update, (), self.request)
        if self.request.response.getStatus() in (302, 303):
            # A redirect was triggered somewhere in update().  Don't
            # continue processing the form
            return

        self.updateForm()
        if self.request.response.getStatus() in (302, 303):
            return
        
        if self.request.get('ajax'):
            return "<html> %s </html>" %self.content()

        self.layout = component.getMultiAdapter(
            (self.request, self.context), ILayout)
        return self.layout(self)


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

    def validateData(self, fields, data, errors):
        super(MyForm, self).validateData(fields, data, errors)
        if data.get('name') == "hans":
            errors.append(uvcsite.Error('Hans ist doof', identifier=self.prefix))
        return errors

    def update(self):
        self.setContentData(uvcsite.DictDataManager(dict(name="Klaus")))
        double.need()
        DatePickerCSS.need()
        uvcsite.Overlay.need()
        validation.need()
        DatePicker.need()
        uvcsite.Tooltip.need()

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        if errors or self.errors:
            self.flash(u"FEHLER", type="error")
            return
        self.flash('Alles Klar')


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


class ISimplePerson(interface.Interface):

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

from zope.component.interfaces import IFactory

class SimplePerson(uvcsite.Content):
    uvcsite.schema(ISimplePerson)


grok.global_utility(SimplePerson, 
    name='uvcsite.tests.forms.ISimplePerson',
    direct=True,
    provides=IFactory)


class IAdressen(interface.Interface):

    personen = schema.List(
        title=u"Personen",
        description=u"Bitte tragen Sie alle Personen ein...",
        value_type=schema.Object(
            title=u"Person", 
            schema=ISimplePerson),
        )
        

class ComplexForm(uvcsite.Form):
    """ """
    grok.title(u'KomplexForm')
    grok.description(u"Komplexe Form")
    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(FormBeispiele)

    ignoreContent = False 
    ignoreRequest = False
    fields = uvcsite.Fields(IAdressen)

    label = u"Adressen"
    description = u"Adressen"

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
