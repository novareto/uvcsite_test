# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok

from uvcsite.interfaces import IUVCSite, ISidebar
from zope.interface import Interface
from zope.schema import TextLine, Choice
from megrok.z3cform.base import PageForm, Fields, button
from dolmen.menu import menuentry
from z3c.form.browser.radio import RadioFieldWidget 


class IPerson(Interface):

    name = TextLine(
       title = u"Name",
       description = u"Bitte geben Sie hier den Namen ein",
       )

    vorname = TextLine(
        title = u"Vorname",
        description = u"Bitte geben Sie den Vornamen ein",
        )

    geschlecht = Choice(
        title = u"Gender",
        description = u"Bitte geben Sie das Geschlecht ein",
        values = ('men', 'woman'),
        )

@menuentry(ISidebar)
class MyForm(PageForm):
    grok.title(u'Beispielform')
    grok.context(IUVCSite)
    ignoreContext = True
    fields = Fields(IPerson)
    fields['geschlecht'].widgetFactory = RadioFieldWidget

    @button.buttonAndHandler(u'EGON')
    def handleButton(self, action):
       data, errors = self.extractData()
       if errors:
           self.flash(self.formErrorsMessage, type="error")
           return
       self.flash('Alles Klar')
       return 
