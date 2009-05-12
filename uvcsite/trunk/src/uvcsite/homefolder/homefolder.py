# -*- coding: utf-8 -*-

import grok
import megrok.pagelet

from uvcsite import uvcsiteMF as _
from uvcsite.interfaces import IHomeFolder
from zope.interface import Interface
from zope.component import getMultiAdapter

from zope.app.interface import queryType
from zope.app.content.interfaces import IContentType
from zope.app.homefolder.homefolder import HomeFolderManager
from zope.app.homefolder.interfaces import IHomeFolderManager

class HomeFolder(grok.Container):
    grok.implements(IHomeFolder)
    pass

class Members(grok.Container):
    pass

class PortalMembership(HomeFolderManager):
    """ """
    grok.implements(IHomeFolderManager)

    def __init__(self):
        super(PortalMembership, self).__init__()
        self.homeFolderBase = Members()
	self.autoCreateAssignment = True
	self.homeFolderRole = u'uvc.ManageHomeFolder'
        self.containerObject = 'uvcsite.homefolder.homefolder.HomeFolder'


class HomeFolderIndex(megrok.pagelet.Pagelet):
    grok.name('index')
    grok.require('uvc.AccessHomeFolder')
    grok.context(IHomeFolder)
    
    # This shows which metatype is called
    meta_type = None
    description = _(u"Hier werden Ihre Dokumente abgelegt")

    @property
    def title(self):
	#print self.request.principal
	name = self.request.principal.title
        return _(u"Ordner von %s" %name)

    def getContentTypes(self):
	""" Return the different Content Types in this Folder"""
	rc = []
	for object in self.context.values():
	    meta_type = getattr(object, 'meta_type', '')
	    if not meta_type in rc and meta_type != '':
		rc.append(meta_type)
	return rc    


    def update(self, meta_type=None):
	self.meta_type = meta_type

    def renderBatch(self):
	context = self.context
	table = getMultiAdapter((self.context, self.request), name="table")
	table.__name__ = context.__name__
	table.__parent__ = context.__parent__
	table.update()
	table.updateBatch()
	return table.renderBatch()

    def renderTable(self):
	table = getMultiAdapter((self.context, self.request), name="table")
	table.update()
	return table.renderTable()

class DeleteItem(grok.View):
    grok.context(IHomeFolder)
    """ Delete the DATA"""

    def update(self):
	context = self.context
	for x in self.request.get('table-checkbox-0-selectedItems',[]):
	    del context[x]

    def render(self, **kw):
        return ''

