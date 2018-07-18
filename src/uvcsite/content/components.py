import grok
import dolmen.content
import zope.security

from zope.schema import TextLine
from uvcsite.content.interfaces import IContent, IProductFolder, IFolderColumnTable
from zope.interface import implements
from uvcsite.content.directive import contenttype
from grokcore.component import directive
from zope.container.interfaces import INameChooser
from zope.dublincore.interfaces import IZopeDublinCore
from zope.pluggableauth.factories import Principal


class ProductFolder(grok.Container):
    grok.implements(IProductFolder, IFolderColumnTable)

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

    @property
    def excludeFromNav(self):
        return False


class Content(dolmen.content.Content):
    implements(IContent)
    grok.baseclass()
    dolmen.content.nofactory()

    @property
    def meta_type(self):
        return self.__class__.__name__

    @property
    def schema(self):
        return dolmen.content.schema.bind().get(self)

    @property
    def principal(self):
        dc = IZopeDublinCore(self)
        if len(dc.creators) > 0:
            pid = dc.creators[0]
            return Principal(pid, pid)
        return zope.security.management.getInteraction().participations[0].principal

    @property
    def modtime(self):
        dc = IZopeDublinCore(self)
        return dc.modified
