import grok
import transaction
import uvcsite
import zope.app.appsetup.interfaces
from zope.app.component.hooks import getSite, setSite
from zope.component import getUtility
from zope.app.publication.zopepublication import ZopePublication
from zope.app.homefolder.interfaces import IHomeFolderManager

from zope.component import getUtilitiesFor
from uvcsite.content import IProductFolder, IUVCApplication


@grok.subscribe(zope.app.appsetup.interfaces.IDatabaseOpenedWithRootEvent)
def handle_init(event):
    connection = event.database.open()
    for object in connection.root()[ZopePublication.root_name].values():
        if IUVCApplication.providedBy(object):
            old_site = getSite()
            setSite(object)
            try:
                productfolders = list(getUtilitiesFor(IProductFolder))
                folders = getUtility(IHomeFolderManager).homeFolderBase
                for folder in folders.values():
                    for name, class_ in productfolders:
                        if name in folder:
                            continue
                        folder[name] = class_()
            finally:
                setSite(old_site)
    transaction.commit()
    connection.close()


@grok.subscribe(uvcsite.IMyHomeFolder, grok.IObjectAddedEvent)
def handle_homefolder(homefolder, event):
    productfolders = list(getUtilitiesFor(IProductFolder))
    for name, class_ in productfolders:
        homefolder[name] = class_()
