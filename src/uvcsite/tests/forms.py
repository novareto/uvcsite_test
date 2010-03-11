# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok

from uvcsite.interfaces import IUVCSite, ISidebar
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

from z3c.form import group

class NameGroup(group.Group):
    label = u"Name"
    fields = Fields(IPerson).select(
        'name', 'vorname')

class OtherGroup(group.Group):
    label = u"Other"
    fields = Fields(IPerson).select(
        'geschlecht', 'datum')


@menuentry(ISidebar)
class GroupF(group.GroupForm, PageForm):
    grok.title(u'GroupForm')
    grok.context(IUVCSite)
    fields = Fields(IPerson).select('id')
    groups = (NameGroup, OtherGroup)
    ignoreContext = True

    def updateForm(self):
        """Update the form, i.e. process form input using widgets.

        On z3c.form forms, this is what the update() method is.
        In grok views, the update() method has a different meaning.
        That's why this method is called update_form() in grok forms.
        """
        super(group.GroupForm, self).update()


    @button.buttonAndHandler(u'EGON')
    def handle_add(self,action):
        print "GON"
        return 

    def create(self, data):
        import pdb; pdb.set_trace() 
        print "create"
        return object()

    def add(self, object):
        print "add"
        pass


@menuentry(ISidebar)
class MyForm(PageForm):
    grok.title(u'Beispielform')
    grok.context(IUVCSite)
    ignoreContext = False 
    fields = Fields(IPerson)
    fields['geschlecht'].widgetFactory = RadioFieldWidget

    def getContent(self):
        return dict(name="Klaus")

    @button.buttonAndHandler(u'EGON')
    def handleButton(self, action):
       data, errors = self.extractData()
       if errors:
           self.flash(self.formErrorsMessage, type="error")
           return
       self.flash('Alles Klar')
       return 
