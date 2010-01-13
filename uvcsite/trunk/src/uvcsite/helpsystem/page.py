# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from zope.interface import Interface
from megrok.z3cform.base import (PageAddForm, 
                   PageEditForm, PageDisplayForm, Fields)

from uvcsite import uvcsiteMF as _
from uvcsite import Content, ApplicationAwareView
from uvcsite.interfaces import IDocumentActions
from megrok.layout.components import Form
from uvcsite.helpsystem.interfaces import IHelpFolder, IHelpPage
from uvcsite.content import Content, schema
from uvcsite.helpsystem.portlet import HelpPortlet
from uvcsite.viewlets.utils import DocumentAction


class HelpPage(Content):
    grok.implements(IHelpPage)
    grok.name('HelpPage')
    schema(IHelpPage)

    def __init__(self, name="", title="", text=""):
        self.name = unicode(name)
        self.title = unicode(title)
        self.text = unicode(text)


class Add(PageAddForm, ApplicationAwareView):
    grok.context(IHelpFolder)
    fields = Fields(IHelpPage)
    grok.require('zope.ManageSite')

    label = _(u"Hilfe Seiten anlegen")

    def create(self, data):
        return HelpPage(**data)

    def add(self, object):
        container = self.context
        container[object.name] = object
        return object

    def nextURL(self):
        self.flash(_(u'Die Hilfeseite wurde erfolgreich angelegt'))
        return self.url(self.context)


class Edit(PageEditForm, ApplicationAwareView):
    grok.context(IHelpPage)
    fields = Fields(IHelpPage).omit('name')
    grok.require('zope.ManageSite')



class HelpPageIndex(PageDisplayForm, ApplicationAwareView):
    grok.name('overview')
    grok.context(IHelpPage)
    grok.require('zope.View')
    fields = Fields(IHelpPage)


class TTDisplay(grok.View):
    grok.name('index')
    grok.context(HelpPage)
    grok.require('zope.View')


class HilfePortlet(HelpPortlet):
    """ Portlet Hilfe"""
    grok.context(IHelpFolder)

    urls = [ {'href':'klaus','name':'hilfe'}, ]


# Document Actions

class PdfIcon(DocumentAction):
    grok.name(_(u'aspdf'))
    grok.context(HelpPage)
    grok.viewletmanager(IDocumentActions)

    image = "pdf.png"
    title = (_(u'aspdf'))
    urlEndings = 'aspdf'
    viewURL = 'aspdf'


class AsPdf(grok.View):
    grok.context(HelpPage)
    grok.title('aspdf')

    def render(self):
        return "This should be a PDF"
