# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

from zeam.form.base import action, Form, Fields, DictDataManager
from zope.interface import Interface
from zope import schema
import grok
import uvcsite



class IPerson(Interface):

    name = schema.TextLine(
       title = u"Name",
       description = u"Name",
    )


    birtdate = schema.Date(
        title = u"Birthdate",
        description = u"Birthdate",
    )

    best = schema.Bool(
        title = u"Bestätigung"
    )


class DateForm(uvcsite.Form):
    grok.title(u'Beispielform')
    grok.description(u"Beschreibugn Beschreibugn")
    grok.context(Interface)
    fields = Fields(IPerson)
    fields['best'].mode = "hiddendisplay"
    ignoreContent = False

    def update(self):
        defaults = dict(name=u"Christian", best=False)
        self.setContentData(
            DictDataManager(defaults))

    @action(u'Abschicken')
    def handleButton(self):
        data, errors = self.extractData()
        print data, errors
