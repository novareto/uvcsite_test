# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from megrok.z3cform import PageAddForm, field, PageEditForm, PageDisplayForm

from uvcsite import Content
from megrok.layout.components import Form
from uvcsite.helpsystem.interfaces import IHelpFolder, IHelpPage
from uvc.content import Content, schema

class HelpPage(Content):
    grok.implements(IHelpPage)
    schema(IHelpPage)

    def __init__(self, name="", title="", text=""):
        self.name = unicode(name)
        self.title = unicode(title)
        self.text = unicode(text)


class HelpAdd(PageAddForm):
    grok.context(IHelpFolder)
    fields = field.Fields(IHelpPage)
    grok.require('zope.ManageSite')

    label = u"Hilfe Seiten anlegen"

    def create(self, data):
        return HelpPage(**data)

    def add(self, object):
        container = self.context
        container[object.name] = object
        return object

    def nextURL(self):
        self.flash(u'Die Hilfeseite wurde erfolgreich angelegt')
        return self.url(self.context)


class Edit(PageEditForm):
    grok.context(IHelpPage)
    fields = field.Fields(IHelpPage).omit('name')
    grok.require('zope.ManageSite')


class HelpPageIndex(PageDisplayForm):
    grok.name('overview')
    grok.context(IHelpPage)
    grok.require('zope.View')
    fields = field.Fields(IHelpPage)


class TTDisplay(grok.View):
    grok.name('index')
    grok.context(HelpPage)
    grok.require('zope.View')
