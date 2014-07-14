# -*- coding: utf-8 -*-

import uvclight
import dolmen.content
import zope.security

from dolmen.container.components import BTreeContainer
from cromlech.container.interfaces import INameChooser
from grokcore.component import directive
from uvcsite.content.directive import contenttype
from uvcsite.content.interfaces import IContent, IProductFolder, IFolderColumnTable
from zope.schema import TextLine


class ProductFolder(BTreeContainer):
    uvclight.implements(IProductFolder, IFolderColumnTable)

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
    uvclight.implements(IContent)
    uvclight.baseclass()

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
