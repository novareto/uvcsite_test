# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from grokcore.component import provider
from zope.interface import Interface
from zope.schema import Choice

from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from grokcore.chameleon.components import ChameleonPageTemplateFile


@provider(IContextSourceBinder)
def jobs(context):
    return SimpleVocabulary([SimpleTerm('Bitte Auswahl treffen.', 'Bitte Auswahl treffen.'),])


class IExampleForm(Interface):

    berufe = Choice(
        title=u"Berufe",
        description=u"Bitte wählen Sie zunächst Ihre Sparte und anschließend\
        einen entsprechenden Beruf",
        source=jobs
    )


class ExampleForm(uvcsite.Form):
    grok.context(uvcsite.IUVCSite)
    grok.name('ef')
    grok.require('zope.Public')

    fields = uvcsite.Fields(IExampleForm)

    @property
    def mastervalues(self):
        return ('bbg', 'stbg', 'lpz')

    def updateForm(self):
        super(ExampleForm, self).updateForm()
        self.fieldWidgets.get('form.field.berufe').template = ChameleonPageTemplateFile('templates/ms.cpt')

    @uvcsite.action(u'Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        print data


class MasterSelect(grok.JSON):
    grok.context(ExampleForm)
    grok.view(ExampleForm)

    def select(self, master):
        if master == "stbg":
            rc = "<option value='STBG'> STBG-BERUFE</option>"
        else:
            rc = "<option value='BBG'> BBG-Berufre</option"
        return {'options': rc}
