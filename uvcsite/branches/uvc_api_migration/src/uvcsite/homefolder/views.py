## # -*- coding: utf-8 -*-
## # Copyright (c) 2007-2008 NovaReto GmbH
## # cklinger@novareto.de

import uvclight
import uvcsite

from megrok.z3ctable import Values
from uvc.layout import interfaces
from uvcsite import uvcsiteMF as _
#from uvcsite.content.productregistration import getAllProductRegistrations
#from uvcsite.homefolder.homefolder import Members
from uvcsite.interfaces import IMyHomeFolder, IFolderListingTable
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.pagetemplate.interfaces import IPageTemplate
from zope.traversing.browser import absoluteURL


## uvclight.templatedir('templates')


class Index(uvclight.TablePage):
    uvclight.title(u'Mein Ordner')
    uvclight.context(IMyHomeFolder)
    uvclight.implements(IFolderListingTable)
    #uvcsite.sectionmenu(uvcsite.IExtraViews)

    cssClasses = {
        'table': 'tablesorter table table-striped ' +
                 'table-bordered table-condensed',
        }
    cssClassEven = u'even'
    cssClassOdd = u'odd'

    startBachtAt = 15
    bachtSize = 15
    sortOn = "table-modified-5"

    @property
    def title(self):
        name = self.request.principal.title
        return _(u"Ordner von %s", name)

    description = _(u"Hier werden Ihre Dokumente abgelegt")

    def getContentTypes(self):
        interaction = self.request.interaction
        for key, value in self.context.items():
            if (interaction.checkPermission('uvc.ViewContent', value) and
                not getattr(value, 'excludeFromNav', False)):
                yield dict(href = absoluteURL(value, self.request),
                           name = key)

    def executeDelete(self, item):
        self.flash(_(u'Ihre Dokumente wurden entfernt'))
        del item.__parent__[item.__name__]

    def update(self):
        items = self.request.form.get('table-checkBox-0-selectedItems')
        if items and self.request.has_key('form.button.delete'):
            if isinstance(items, (str, unicode)):
                items = [items,]
            for key in items:
                for pf in self.context.values():
                    if pf.has_key(key):
                        self.executeDelete(pf[key])
        super(Index, self).update()


## class DirectAccessViewlet(uvclight.Viewlet):
##     uvclight.view(IFolderListingTable)
##     uvclight.order(25)
##     uvclight.context(Interface)
##     uvclight.viewletmanager(interfaces.ITabs)

##     def getContentTypes(self):
##         interaction = self.request.interaction
##         hf = uvcsite.getHomeFolder(self.request)
##         for key, value in getAllProductRegistrations():
##             if getattr(value, 'inNav', True):
##                 pf = hf[value.folderURI]
##                 if interaction.checkPermission('uvc.ViewContent', pf):
##                     yield dict(href = absoluteURL(pf, self.request),
##                                name = value.title)

##     def render(self):
##         template = getMultiAdapter((self, self.request), IPageTemplate)
##         return template()


## class DirectAccess(PageTemplate):
##     uvclight.view(DirectAccessViewlet)


## class HomeFolderValues(Values):
##     """This Adapter returns IContent Objects
##        form child folders
##     """
##     uvclight.adapts(IMyHomeFolder, None, Index)

##     @property
##     def values(self):
##         results = []
##         interaction = self.request.interaction
##         for productfolder in self.context.values():
##             if interaction.checkPermission('uvc.ViewContent', productfolder):
##                 results.extend(productfolder.values())
##         return results


## class RedirectIndexMembers(uvclight.View):
##     uvclight.context(Members)
##     uvclight.name('index')

##     def render(self):
##         url = uvcsite.IGetHomeFolderUrl(self.request).getURL()
##         self.redirect(url)

## class RestHomeFolderTraverser(uvclight.Traverser):
##     uvclight.context(Members)
##     uvclight.layer(IRESTLayer)

##     def traverse(self, name):
##         return uvcsite.getHomeFolder(self.request).get(name)
