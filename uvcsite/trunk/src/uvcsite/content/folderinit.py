# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import transaction
import uvcsite
import zope.app.appsetup.interfaces
from zope.site.hooks import getSite, setSite
from zope.component import getUtility
from zope.app.publication.zopepublication import ZopePublication
from zope.app.homefolder.interfaces import IHomeFolderManager

from zope.component import getUtilitiesFor
from uvcsite.content import IProductFolder, IUVCApplication


#@grok.subscribe(zope.app.appsetup.interfaces.IDatabaseOpenedWithRootEvent)
def handle_init(event):
    connection = event.database.open()
    for object in connection.root()[ZopePublication.root_name].values():
        if IUVCApplication.providedBy(object):
            old_site = getSite()
            setSite(object)
            try:
                productfolders = list(getUtilitiesFor(IProductFolder))
                folders = getUtility(IHomeFolderManager).homeFolderBase
                uvcsite.log('Start applying ProductFolders for UVCSite: %s' %len(folders))
                for folder in folders.values():
                    for name, class_ in productfolders:
                        if name in folder:
                            continue
                        folder[name] = class_()
            finally:
                setSite(old_site)
    transaction.commit()
    connection.close()

from uvcsite.content.interfaces import IProductRegistration
from zope.component import getAdapters
from zope.pluggableauth.factories import Principal


def createProductFolders(principal=None):
    request = zope.security.management.getInteraction().participations[0]
    if not principal:
       principal = request.principal
    for name, pr in getAdapters((principal, request), IProductRegistration):
        uvcsite.log('Add Productfolders %s to Homefolder: %s' % (name, principal.id))
        pr.createInProductFolder()


@grok.subscribe(uvcsite.IMyHomeFolder, grok.IObjectAddedEvent)
def handle_homefolder(homefolder, event):
    principal = Principal(homefolder.__name__, homefolder.__name__)
    createProductFolders(principal)
#    uvcsite.log('Add Productfolders to Homefolder: %s' % homefolder.__name__)
#    productfolders = list(getUtilitiesFor(IProductFolder))
#    for name, class_ in productfolders:
#        homefolder[name] = class_()

