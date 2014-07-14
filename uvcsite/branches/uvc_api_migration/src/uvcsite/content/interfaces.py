#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema import TextLine
from dolmen.content import IContent
from zope.interface import Interface
from cromlech.container.interfaces import IContainer


class IUVCApplication(Interface):
    """Marker Interface the application_url method
    """


class IProductFolder(IContainer):
    """MARKER
    """


class IFolderColumnTable(Interface):
    """Provide standard folder columns
    """


class IContent(IContent):

    title = TextLine(
        title = u"Titel",
        description = u"Bitte geben Sie einen Titel für das Dokument an. Dieses Dokument erscheint dann unter dem Titel in Mein Ordner.",
        required = True)


class IProductRegistration(Interface):
    """ Registry for uvcsite.Content objects
    """


