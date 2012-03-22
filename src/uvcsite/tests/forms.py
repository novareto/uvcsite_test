# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from zope import interface
from zope import schema

from zeam.form.base.widgets import getWidgetExtractor
from uvc.widgets import DatePicker, DatePickerCSS, double
from uvc.widgets.fields import OptionalChoice
from zope.i18n import translate


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


class FormBeispiele(uvcsite.SubMenu):
    grok.title('Formulare')
    grok.context(interface.Interface)
    grok.viewletmanager(uvcsite.IGlobalMenu)

from zeam.form.base import Form
from zope import component
from megrok.layout.interfaces import ILayout
from zope.publisher.publish import mapply
from zope.interface import Interface


class StandardFormMenu(uvcsite.MenuItem):
    grok.title('Beispielform')
    grok.viewletmanager(FormBeispiele)

    action = u"myform"




class SimpleForm(uvcsite.Form):
    grok.title('SimpleForm')
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    ignoreContent = False 
    ignoreRequest = False
    fields = uvcsite.Fields(IPerson)

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()



class MyForm(uvcsite.Form):
    grok.title(u'Beispielform')
    grok.description(u"Beschreibugn Beschreibugn")
    grok.context(uvcsite.IUVCSite)

    ignoreContent = False 
    ignoreRequest = False
    fields = uvcsite.Fields(IPerson)
    #fields['geschlecht'].mode = "radio"

    label = u"Beispielform"
    description = u"Beschreibung"
    legend = "LEGENDE"

    def validateData(self, fields, data, errors):
        super(MyForm, self).validateData(fields, data, errors)
        if data.get('name') == "hans":
            errors.append(uvcsite.Error('Hans ist doof', identifier=self.prefix))
        return errors

    def update(self):
        self.setContentData(uvcsite.DictDataManager(dict(name="Klaus")))
        double.need()
        DatePickerCSS.need()
        DatePicker.need()

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
    fields = uvcsite.Fields(IPerson)

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
        

class oComplexForm(uvcsite.Form):
    """ """
    grok.title(u'oKomplexForm')
    grok.description(u"oKomplexe Form")
    grok.context(uvcsite.IUVCSite)
    #uvcsite.menu(FormBeispiele)

    ignoreContent = False 
    ignoreRequest = False
    fields = uvcsite.Fields(IAdressen)

    label = u"Adressen"
    description = u"Adressen"

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        print errors.title

from zeam.form.ztk.widgets.collection import MultiObjectFieldWidget, newCollectionWidgetFactory
from zope.interface import Interface
from zeam.form.ztk.interfaces import ICollectionSchemaField
from zeam.form.ztk.widgets.object import ObjectSchemaField 
from zeam.form.base.interfaces import IWidget 
from zeam.form.base import HIDDEN
from zope import component



class UOFW(MultiObjectFieldWidget):
    grok.adapts(ICollectionSchemaField, ObjectSchemaField, Interface, Interface)
    grok.name('bgdp')

    def getDisplayWidgets(self, widget):
        ww = component.getMultiAdapter(
            (widget.component, widget.form, self.request), 
            IWidget, 
            name='hidden')
        ww.update()
        return "%s %s" %(ww.render(), ww.inputValue())

    @property
    def getValueWidgets(self):
        widgets = [x for x in self.valueWidgets]
        if self.request.has_key(self.identifier + '.add'):
            widgets.pop()
        return widgets 
   
    @property
    def getInputWidget(self):
        if self.request.has_key(self.identifier + '.add'):
            vv= [x for x in self.valueWidgets].pop()
            return [x for x in self.valueWidgets].pop()
        return None 

    @property
    def allowAddingCustom(self):
        return self.request.has_key(self.identifier + '.add')


    def iupdate(self):
        from zeam.form.base.widgets import getWidgetExtractor
        super(UOFW, self).update()
        if self.request.has_key(self.identifier + '.dadd'):
            for field in self.getFields():
                extractor = getWidgetExtractor(self.component, self.form, self.request)
                value, error = extractor.extract()
                print value, error
                if error is None:
                    error = field.validate(value, self.form)



import grokcore.component
from zeam.form.base.interfaces import IField, IWidget
grokcore.component.global_adapter(
    newCollectionWidgetFactory(mode='bgdp'),
    adapts=(ICollectionSchemaField, Interface, Interface),
    provides=IWidget,
    name='bgdp')


