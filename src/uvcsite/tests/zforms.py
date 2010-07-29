
import grok
import uvcsite

from zeam.form import layout
from zeam.form import base
from dolmen.forms.base import Fields
from zope import interface
from zope import schema
from uvc import validation


class IMyFields(interface.Interface):


    name = schema.TextLine(
        title=u"Name", 
        description=u'Beschreibung', 
        required=True,
        constraint = validation.validation.validateZahl
        )

    gender = schema.Choice(
        title = u"Geschlecht",
        description = u"Geschlecht",
        values = ['klaus', 'egon']
        )

class MailForm(uvcsite.Form):
    grok.context(uvcsite.IUVCSite)
    label = u"Send a mail"
    description = u"to people"
    fields = Fields(IMyFields)
    submissionError = None


    def update(self):
        super(MailForm, self).update()
        self.fields.get('gender').mode = 'radio'

    @base.action(u'Senden', 'idsind')
    def send(self):
        data, errors = self.extractData()
        print data
        if errors:
            self.flash(u'Achtung Fehler', 'error')
            return

