# -*- coding: utf-8 -*- 
# Copyright (c) 2007-2008 NovaReto GmbH 
# cklinger@novareto.de 

import grok

from uvcsite.interfaces import IContainer
from zope.interface import Interface
from zope.schema import TextLine, Text

class IHelpFolder(IContainer):
    pass

class IHelpPage(Interface):
    title = TextLine(title=u"title")
    description = TextLine(title=u"description")
    text = Text(title=u"text")

