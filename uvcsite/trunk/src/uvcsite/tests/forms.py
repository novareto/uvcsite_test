# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok

from uvcsite.interfaces import IUVCSite, ISidebar, IGlobalMenu
from zope.interface import Interface
from zope.schema import TextLine, Choice, Date, Object, List
from megrok.z3cform.base import PageAddForm, PageForm, Fields, button
from dolmen.menu import menuentry
from z3c.form.browser.radio import RadioFieldWidget 
from z3c.form.converter import DateDataConverter
import zope.schema.interfaces
from z3c.form.interfaces import IWidget, IDataConverter


class IPerson(Interface):

    id = TextLine(
       title = u"Id",
       description = u"Id",
       )

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
        values = ('men', 'woman', 'kid', 'grandpa', 'sister', 'brother'),
        )

    datum = Date(
        title = u"Datum",
        description = u"Bitte wählen Sie ein Datum aus",
        )

from uvc.widgets import DatePicker, DatePickerCSS, double

@menuentry(IGlobalMenu)
class MyForm(PageForm):
    grok.title(u'Beispielform')
    grok.context(IUVCSite)
    ignoreContext = False 
    fields = Fields(IPerson)
    fields['geschlecht'].widgetFactory = RadioFieldWidget

    def getContent(self):
        return dict(name="Klaus")

    def updateWidgets(self):
        super(MyForm, self).updateWidgets()
        self.widgets['datum'].klass = "datepicker"

    def update(self):
        double.need()

    @button.buttonAndHandler(u'EGON')
    def handleButton(self, action):
       data, errors = self.extractData()
       if errors:
           self.flash(self.formErrorsMessage, type="error")
           return
       self.flash('Alles Klar')
       return 
