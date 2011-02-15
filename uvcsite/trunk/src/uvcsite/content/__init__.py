from zope.schema import TextLine
from uvcsite.content.directive import contenttype 
from dolmen.content import schema, name, IContent
from uvcsite.content.components import ProductFolder, Content
from uvcsite.content.interfaces import IUVCApplication, IProductFolder, IFolderColumnTable


class IContent(IContent):

    title = TextLine(
        title = u"Titel",
        description = u"Bitte geben Sie einen Titel an.",
        required = True)
