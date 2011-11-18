
import grok
import uvcsite

from zeam.form import layout
from zeam.form import base
from dolmen.forms.base import Fields
from zope import interface
from zope import schema
from uvc import validation
from zope.component.interfaces import IFactory


class ITelefonnummern(interface.Interface):

    typ = schema.Choice(
        title=u"Art",
        values=['mobil','fax','arbeit']
        )

    nummer = schema.TextLine(
        title=u"Telefonnummer",
        description=u"Telefonnummer",
        required=True
        )

class IMyFields(interface.Interface):

    name = schema.TextLine(
        title=u"Name", 
        description=u'Beschreibung', 
        required=True,
        constraint = validation.validation.validateZahl
        )

    telefonnummern = schema.List(
        title = u"Telefonnummern",
        description = u"Telefonnummern",
        required = False,
        value_type = schema.Object(
            title=u"Telefonummern",
            schema=ITelefonnummern),
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


class Nummern(grok.Model):
    grok.implements(ITelefonnummern)

    def __init__(self, typ=None, nummer=None):
        self.typ = typ
        self.nummer = nummer

class TelefonnummernFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('uvcsite.tests.zforms.ITelefonnummern')

    def __call__(self, typ=None, nummer=None):
        return  Nummern(typ, nummer)

