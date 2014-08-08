# -*- coding: utf-8 -*-

import uvclight
import dolmen.content
import zope.security

from dolmen.container.components import BTreeContainer
from cromlech.container.interfaces import INameChooser
from grokcore.component import directive
from uvcsite.content.directive import contenttype
from uvcsite.content.interfaces import IContent
from uvcsite.content.interfaces import IProductFolder, IFolderColumnTable
from zope.schema import TextLine
from zope.annotation.interfaces import IAttributeAnnotatable


class Content(uvclight.backends.zodb.Content):
    uvclight.implements(IContent, IAttributeAnnotatable)


class Container(uvclight.backends.zodb.Container):
    uvclight.implements(IContent, IAttributeAnnotatable)


class ProductFolder(BTreeContainer):
    uvclight.implements(IProductFolder, IFolderColumnTable, IAttributeAnnotatable)

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
        name = INameChooser(self).chooseName(
            content.__class__.__name__ or '', content)
        self[name] = content

    @property
    def excludeFromNav(self):
        return False


class Content(uvclight.backends.zodb.Content):

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
        return uvclight.current_principal()

    @property
    def modtime(self):
        dc = IZopeDublinCore(self)
        return dc.modified
