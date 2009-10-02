# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from zope.interface import Interface
from megrok.z3cform.base import PageAddForm, field, PageEditForm, PageDisplayForm, Fields

from uvcsite import Content, ApplicationAwareView
from uvcsite.skin.skin import Forms 
from megrok.layout.components import Form
from uvcsite.helpsystem.interfaces import IHelpFolder, IHelpPage
from uvcsite.content import Content, schema

class HelpPage(Content):
    grok.implements(IHelpPage)
    schema(IHelpPage)

    def __init__(self, name="", title="", text=""):
        self.name = unicode(name)
        self.title = unicode(title)
        self.text = unicode(text)


class HelpAdd(PageAddForm, ApplicationAwareView):
    grok.context(IHelpFolder)
    fields = Fields(IHelpPage)
    grok.require('zope.ManageSite')

    label = u"Hilfe Seiten anlegen"

    def update(self):
        Forms.need()

    def create(self, data):
        return HelpPage(**data)

    def add(self, object):
        container = self.context
        container[object.name] = object
        return object

    def nextURL(self):
        self.flash(u'Die Hilfeseite wurde erfolgreich angelegt')
        return self.url(self.context)


class Edit(PageEditForm, ApplicationAwareView):
    grok.context(IHelpPage)
    fields = Fields(IHelpPage).omit('name')
    grok.require('zope.ManageSite')

    def update(self):
        Forms.need()


class HelpPageIndex(PageDisplayForm, ApplicationAwareView):
    grok.name('overview')
    grok.context(IHelpPage)
    grok.require('zope.View')
    fields = Fields(IHelpPage)


class TTDisplay(grok.View):
    grok.name('index')
    grok.context(HelpPage)
    grok.require('zope.View')
