# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite


from zope import interface, schema
from zope.component.interfaces import IFactory
from grokcore.chameleon.components import ChameleonPageTemplateFile


class ISimplePerson(interface.Interface):

    name = schema.TextLine(
        title=u"Name",
        required=True,
        description=u"Bitte geben Sie hier den Namen ein",
    )

    vorname = schema.Int(
        title=u"Vorname",
        description=u"Bitte geben Sie den Vornamen ein",
    )

    geschlecht = schema.Choice(
        title=u"Gender",
        description=u"Bitte geben Sie das Geschlecht ein",
        values=('m', 'w'),
    )


class SimplePerson(uvcsite.Content):
    uvcsite.schema(ISimplePerson)


grok.global_utility(
    SimplePerson,
    name='uvcsite.tests.bgvform.ISimplePerson',
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


class BGVExampleForm(uvcsite.Form):
    """ """
    grok.name('bgvform')
    grok.title(u'oKomplexForm')
    grok.description(u"oKomplexe Form")
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.Public')

    fields = uvcsite.Fields(IAdressen)
    fields['personen'].allowOrdering = False
    fields['personen'].inlineValidation = True

    label = u"Adressen"
    description = u"Adressen"

    def updateForm(self):
        super(BGVExampleForm, self).updateForm()
        self.fieldWidgets.get('form.field.personen').template = ChameleonPageTemplateFile('templates/bgv.cpt')

    @uvcsite.action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        print errors.title
