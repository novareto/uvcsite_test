# -*- coding: utf-8 -*-

import grok
import megrok.pagelet

from uvcsite import uvcsiteMF as _
from uvcsite.interfaces import IHomeFolder
from uvcsite.auth.interfaces import IMasterUser
from zope.interface import Interface
from zope.component import getMultiAdapter

from zope.app.interface import queryType
from zope.app.content.interfaces import IContentType
from zope.app.homefolder.homefolder import HomeFolderManager
from zope.app.homefolder.interfaces import IHomeFolderManager
import zope.app.homefolder.homefolder
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.dottedname.resolve import resolve
from zope.security.interfaces import IPrincipal

class HomeFolder(grok.Container):
    grok.implements(IHomeFolder)

class Members(grok.Container):
    pass

class PortalMembership(HomeFolderManager):
    """ """
    grok.implements(IHomeFolderManager)

    autoCreateAssignment = True
    homeFolderRole = [u'uvc.User', u'uvc.Editor', u'uvc.MasterUser']
    containerObject = 'uvcsite.homefolder.homefolder.HomeFolder'

    def assignHomeFolder(self, principalId, folderName=None, create=None):
        """See IHomeFolderManager"""
        # The name of the home folder is folderName, if specified, otherwise
        # it is the principal id
        name = folderName or principalId
        # Make the assignment.
        self.assignments[principalId] = name

        # Create a home folder instance, if the correct flags are set.
        if (create is True) or (create is None and self.createHomeFolder):
            if name not in self.homeFolderBase:
                objectToCreate = resolve(self.containerObject)
                self.homeFolderBase[name] = objectToCreate()
            principal_roles = IPrincipalRoleManager(self.homeFolderBase[name])
            for role in self.homeFolderRole:
                principal_roles.assignRoleToPrincipal(
                    role, principalId)


    @property
    def homeFolderBase(self):
	return grok.getSite()['members'] 

class HomeFolderForPrincipal(grok.Adapter, zope.app.homefolder.homefolder.HomeFolder):
    grok.context(IPrincipal)
    def __init__(self, principal):
        self.principal = IMasterUser(principal) 



@grok.subscribe(IHomeFolderManager, grok.IObjectAddedEvent)
def add_members_folder(object, event):
    object.__parent__.__parent__['members'] = Members()

class HomeFolderIndex(megrok.pagelet.Pagelet):
    grok.name('index')
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

