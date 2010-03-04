# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

from uvcsite import IContent
from zope.schema import TextLine, Text
from uvcsite.interfaces import IFolderColumnTable


class IHelpFolder(IFolderColumnTable):
    pass


class IHelpPage(IContent):
    """A help page prototype.
    """
    name = TextLine(
        title=u"Name",
        description=u"Bitte hier die Daten eingeben",
        )

    title = TextLine(
        title=u"title",
        description=u"Bitte hier die Daten eingeben",
        )

    text = Text(
        title=u"text",
        description=u"Bitte hier die Daten eingeben",
        )
