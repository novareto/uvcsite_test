import grok
import dolmen.content

from zope.dottedname.resolve import resolve
from uvcsite.content.interfaces import IProductFolder, IFolderColumnTable
from uvcsite.content.directive import contenttype
from zope.schema.fieldproperty import FieldProperty
from grokcore.component import directive
from zope.app.container.interfaces import INameChooser


class ProductFolder(grok.Container):
    grok.implements(IProductFolder, IFolderColumnTable)

    # per Default all ProductFolders should go into
    # the Homefolder on startup
    inHomeFolder = True

    @property
    def name(self):
        return directive.name.bind().get(self)

    @property
    def title(self):
        return directive.title.bind().get(self)

    @property
    def description(self):
        return directive.description.bind().get(self)

    def getContentType(self):
        return contenttype.bind().get(self)

    def getContentName(self):
        return self.getContentType().__content_type__

    def add(self, content):
        name = INameChooser(self).chooseName(content.__name__ or '', content)
        self[name] = content


class Content(dolmen.content.Content):
    grok.baseclass()
    dolmen.content.nofactory()

    @property
    def meta_type(self):
        return self.__class__.__name__

    @property
    def schema(self):
        return dolmen.content.schema.bind().get(self)
