# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite
import uvc.layout
import zope.schema
import zope.interface
import zope.component

from dolmen import menu
from uvc.validation import validation


class IContact(uvcsite.IContent):

    name = zope.schema.TextLine(
        title = u"Name",
        description = u"Wie ist ihr Name",
        )

    alter = zope.schema.TextLine(
        title = u"Alter",
        description = u"Wie ist ihr Alter",
        constraint = validation.validateZahl
        )

class IAdressBook(uvcsite.IProductFolder):
    """ Marker Interface """


class Contact(uvcsite.Content):
    grok.name(u'Kontakt')
    uvcsite.schema(IContact)


class AdressBook(uvcsite.ProductFolder):
    grok.implements(IAdressBook)
    grok.name('adressbook')
    grok.title('Adressbuch')
    grok.description('Adressbuch ...')
    uvcsite.contenttype(Contact)


class StatMenu(uvcsite.MenuItem):
    grok.context(AdressBook)
    grok.viewletmanager(uvcsite.IExtraViews)
    grok.title('Statistik')

    action = "stat"


class Stat(uvcsite.Page):
    grok.name('stat')
    grok.title('Statistik')
    grok.context(AdressBook)

    def render(self):
        return "<div> <h1>Statistiks</h1> </div>"


@grok.subscribe(Contact, uvcsite.IAfterSaveEvent)
def handle_save(obj, event):
    print "AfterSaveEvent"


class AddMenuEntry(uvcsite.MenuItem):
    grok.name('Buddy erstellen')
    grok.title('Buddy erstellen')
    grok.context(zope.interface.Interface)
    grok.viewletmanager(uvcsite.IGlobalMenu)

    @property
    def action(self):
        adapter = zope.component.getMultiAdapter((self.request.principal, self.request), uvcsite.IGetHomeFolderUrl)
        return adapter.getAddURL(Contact)
