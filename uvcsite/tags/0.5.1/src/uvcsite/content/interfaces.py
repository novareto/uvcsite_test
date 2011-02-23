#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.schema import TextLine
from dolmen.content import IContent
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


class IContent(IContent):

    title = TextLine(
        title = u"Titel",
        description = u"Bitte geben Sie einen Titel an.",
        required = True)
