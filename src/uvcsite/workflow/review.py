import grok
import uvcsite


from zope import interface
from uvcsite.homefolder.views import Index
from uvcsite.auth.interfaces import ICOUser
from megrok.z3ctable import (table, Column)
from uvcsite.interfaces import IFolderColumnTable
from hurry.workflow.interfaces import IWorkflowState
from uvcsite.workflow.basic_workflow import REVIEW


class ReviewViewlet(grok.Viewlet):
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.context(interface.Interface)
    grok.baseclass()

    def available(self):
        if (len(self.values) > 0 and
            not ICOUser.providedBy(self.request.principal)):
            return True
        return False

    @property
    def values(self):
        results = []
        homefolder = uvcsite.getHomeFolder(self.request)
        if homefolder:
            interaction = self.request.interaction
            for productfolder in homefolder.values():
                if not productfolder.__name__.startswith('__'):
                    if interaction.checkPermission(
                            'uvc.ViewContent', productfolder):
                        results = [x for x in productfolder.values()
                                   if IWorkflowState(x).getState() == REVIEW]
        return results

    def render(self):
        return (u"<p class='alert'> Sie haben (%s) " +
                u"Dokumente in Ihrer <a href='%s'> ReviewList. </a> </p>") % (
                    len(self.values),
                    uvcsite.getHomeFolderUrl(self.request, 'review_list'))


class ReviewList(Index):
    grok.name('review_list')
    grok.require('uvc.EditContent')
    grok.baseclass()

    @property
    def values(self):
        results = []
        homefolder = uvcsite.getHomeFolder(self.request)
        if homefolder:
            interaction = self.request.interaction
            for productfolder in homefolder.values():
                if not productfolder.__name__.startswith('__'):
                    if interaction.checkPermission(
                            'uvc.ViewContent', productfolder):
                        results = [x for x in productfolder.values()
                                   if IWorkflowState(x).getState() == REVIEW]
        return results


class ModifiedColumn(Column):
    grok.name('modified')
    grok.context(IFolderColumnTable)
    header = u"Freigeben"
    weight = 100
    table(ReviewList)

    def renderCell(self, item):
        url = grok.url(self.request, item, name="publish")
        return "<a href='%s'> Freigeben </a>" % url
