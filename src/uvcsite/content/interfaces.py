#!/usr/bin/python
# -*- coding: utf-8 -*-

import dolmen.content
from zope.schema import TextLine
from zope.interface import Interface
from grok.interfaces import IContainer


class IUVCApplication(Interface):
    """Marker Interface the application_url method
    """


class IProductFolder(IContainer):
    """MARKER
    """


class IFolderColumnTable(Interface):
    """Provide standard folder columns
    """


class IContent(dolmen.content.IContent):

    title = TextLine(
        title=u"Titel",
        description=(
            u"Bitte geben Sie einen Titel für das Dokument an. " +
            u"Dieses Dokument erscheint dann unter dem Titel in Mein Ordner."),
        required=True)


class IProductRegistration(Interface):
    """Registry for uvcsite.Content objects
    """
