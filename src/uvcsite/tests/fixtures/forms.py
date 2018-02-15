# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope import interface
from zope import schema

from uvc.widgets import double, masked_input
from zeam.form.base.widgets import getWidgetExtractor
from uvc.widgets.fields import OptionalChoice
from zope.i18n import translate
from zeam.form.base import Form
from zope import component
from grokcore.layout.interfaces import ILayout
from zope.publisher.publish import mapply
from zope.interface import Interface
#from zeam.form.ztk import customize
from uvc.validation import validation


class IPerson(interface.Interface):

    id = schema.TextLine(
        title = u"Id",
        description = u"Id",
        max_length=3,
        constraint = validation.validateZahl,
        )

    check = schema.Bool(
        title=u"Bestaetigung"
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
        title = u"Geschlecht",
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
        required = False,
        )


class FormBeispiele(uvcsite.SubMenu):
    grok.title('Formulare')
    grok.context(interface.Interface)
    grok.viewletmanager(uvcsite.IGlobalMenu)



class StandardFormMenu(uvcsite.MenuItem):
    grok.title('Beispielform')
    grok.viewletmanager(FormBeispiele)

    action = u"myform"


class IFrage(Interface):
    frage = schema.TextLine(title=u"Frage")


class SimpleForm(uvcsite.Form):
    grok.title('SimpleForm')
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    ignoreContent = False
    ignoreRequest = False
    fields = uvcsite.Fields(IFrage)
    frage = u"0"

    def update(self):
        from js.jquery_maskmoney import jquery_maskmoney
        jquery_maskmoney.need()
        print "neeed"

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        print data
        if errors:
            return
        self.frage = data.get('frage')


from zeam.form.table import SubTableForm, TableActions

from zeam.form.base import Action, SUCCESS, Actions

class MailAction(Action):

   def __call__(self, form, selected, deselected):
       # Send a mail
       form.status = u"Mail sent"
       return SUCCESS



class TF(uvcsite.GroupForm):
    grok.title(u'FieldsetBasedForm')
    grok.context(uvcsite.IUVCSite)

    @uvcsite.action(u'Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        print data, errors


class TForm(SubTableForm):
    grok.title('TableForm')
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')
    grok.view(TF)
    prefix = "G"

    tableFields = uvcsite.Fields(IFrage)
    tableActions = TableActions(MailAction(u'dd'))

    @uvcsite.action(u'Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        print data, errors

    def getItems(self):
        return [dict(frage=1), dict(frage=2), dict(frage=3)]


class MyForm(uvcsite.Form):
    grok.title(u'Beispielform')
    grok.description(u"Beschreibugn Beschreibugn")
    grok.context(Interface)

    ignoreContent = False
    ignoreRequest = False
    fields = uvcsite.Fields(IPerson)
    fields['geschlecht'].mode = "radio"
    fields['name'].htmlAttributes['maxlength'] = 10
    fields['vorname'].htmlAttributes['placeholder'] = u"BLA"
    fields['datum'].htmlAttributes = {'placeholder': 'tt.mm.jjjj'}
    fields['check'].htmlAttributes = {'disabled': 'disabled'}
    fields['datum'].mode = "dp-date"

    label = u"Beispielform"
    description = u"Beschreibung"
    legend = "LEGENDE"

    def update(self):
        self.setContentData(uvcsite.DictDataManager(dict(name="Klaus")))
        double.need()
        masked_input.need()

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        if errors or self.errors:
            self.flash(u"FEHLER", type="error")
            return
        self.flash('Alles Klar')


#@customize(schema=IPerson, name="name")
#def handle_name(field):
#    field.htmlAttributes['maxlength'] = 3


class MyFormHilfe(uvcsite.HelpPage):
    grok.context(uvcsite.IUVCSite)
    grok.view(MyForm)


#
## GroupForm
#


class GroupFormMenu(uvcsite.MenuItem):
    grok.title('Gruppen')
    grok.viewletmanager(FormBeispiele)

    action = u"splitcontact"



class SplitContact(uvcsite.GroupForm):
    grok.title(u'FieldsetBasedForm')
    grok.context(uvcsite.IUVCSite)


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
    fields = uvcsite.Fields(IPerson).omit('name')

    label = "Mother"

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()

#
## Wizard
#

class WizardMenu(uvcsite.MenuItem):
    grok.viewletmanager(FormBeispiele)
    grok.title('Wizard')

    @property
    def action(self):
        return "%s/mywizard" %self.view.application_url()


class MyWizard(uvcsite.Wizard):
    grok.title('Wizard')
    grok.context(uvcsite.IUVCSite)
    label = u"Wizard"
    description = u"Ein Beispiel WIZARD"

    def __init__(self, context, request):
        super(MyWizard, self).__init__(context, request)
        #self.setContentData(DictDataManager({}))

    def finish(self):
        pass

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


from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
import grokcore.component as grok
from zope import schema

@grok.provider(schema.interfaces.IContextSourceBinder)
def kk(context):
    terms = []
    for gwz in range(5):
        terms.append( SimpleTerm(gwz, gwz, gwz) )
    return SimpleVocabulary(terms)

class ISimplePerson(interface.Interface):

    name = schema.TextLine(
       title = u"Name",
       required=True,
       description = u"Bitte geben Sie hier den Namen ein",
       )

    vorname = schema.Int(
        title = u"Vorname",
        description = u"Bitte geben Sie den Vornamen ein",
        )

    geschlecht = schema.Choice(
        title = u"Gender",
        description = u"Bitte geben Sie das Geschlecht ein",
        source = kk,
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

class IAdressen1(interface.Interface):

    personen = schema.Object(
            title=u"Person",
            schema=ISimplePerson)



class ComplexForm(uvcsite.Form):
    """ """
    grok.title(u'KomplexForm')
    grok.description(u"Komplexe Form")
    grok.context(uvcsite.IUVCSite)
    #uvcsite.menu(FormBeispiele)

    ignoreContent = False
    ignoreRequest = False
    fields = uvcsite.Fields(IAdressen)
    #fields['personen'].mode = "bgdp"
    fields['personen'].allowOrdering = False
    fields['personen'].inlineValidation = True

    label = u"Adressen"
    description = u"Adressen"

    def update(self):
        super(ComplexForm, self).update()

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        print errors
        import pdb; pdb.set_trace()


class BGVExampleForm(uvcsite.Form):
    """ """
    grok.name('sform')
    grok.title(u'oKomplexForm')
    grok.description(u"oKomplexe Form")
    grok.context(uvcsite.IUVCSite)

    ignoreContent = False
    ignoreRequest = False
    fields = uvcsite.Fields(IAdressen)

    label = u"Adressen"
    description = u"Adressen"

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        print errors.title

