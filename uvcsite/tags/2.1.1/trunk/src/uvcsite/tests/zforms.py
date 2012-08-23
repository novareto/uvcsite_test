# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 


import grok
import uvcsite

from zeam.form import layout
from zeam.form import base
from dolmen.forms.base import Fields
from zope import interface
from zope import schema
from uvc import validation
from zope.component.interfaces import IFactory


class IGewerbszweig(interface.Interface):

    text = schema.TextLine(title=u"Text")
    datum = schema.TextLine(title=u"Datum")
    personen = schema.Int(title=u"Personen")
    entgelt = schema.Int(title=u"Entgelt")


class IBGewerbszweig(interface.Interface):

    gwz = schema.Choice(title=u"Gewerbszweig", values=['a', 'b', 'c'])
    datum = schema.TextLine(title=u"EndeDatum")


class IMyFields(interface.Interface):

    name = schema.TextLine(
        title=u"Name", 
        description=u'Beschreibung', 
        required=True,
        constraint = validation.validation.validateZahl
        )

    ngwzs = schema.List(
        title = u"Neue Gewerbszweige",
        description = u"Bitte klicken Sie auf Hinzufügen falls neue Gewerbszweige hinzugekommen sind.",
        required = False,
        value_type = schema.Object(
            title=u"Gewerbszweige",
            schema=IGewerbszweig),
        )

    bgwzs = schema.List(
        title = u"Beendete Gewerbszweige",
        description = u"Bitte klicken Sie auf Hinzufügen falls Sie Gewerbszweige löschen wollen.",
        required = False,
        value_type = schema.Object(
            title=u"Gewerbszweige",
            schema=IBGewerbszweig),
        )

class MailForm(uvcsite.Form):
    grok.context(uvcsite.IUVCSite)
    label = u"Send a mail"
    description = u"to people"
    fields = Fields(IMyFields)

    @base.action(u'Senden', 'idsind')
    def send(self):
        data, errors = self.extractData()
        print data
        print errors


class Gewerbszweig(grok.Model):
    grok.implements(IGewerbszweig)

    def __init__(self, text=None, datum=None, personen=None, entgelt=None):
        self.text = text
        self.datum = datum
        self.personen = personen
        self.entgelt = entgelt

class GewerbszweigFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('uvcsite.tests.zforms.IGewerbszweig')

    def __call__(self, **kw):
        return  Gewerbszweig(**kw)

