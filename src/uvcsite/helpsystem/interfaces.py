from zope.interface import Interface
from zope.schema import TextLine, Text

class IHelpFolder(Interface):
    pass

class IHelpPage(Interface):
    title = TextLine(title=u"title")
    description = TextLine(title=u"description")
    text = Text(title=u"text")

