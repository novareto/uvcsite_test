# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import uvclight
import uvcsite
import zope.security

from cromlech.browser import IRequest
from uvcsite.content.directive import productfolder
from uvcsite.content.interfaces import IProductRegistration
from uvcsite.content.meta import default_name
from uvcsite.utils.shorties import getHomeFolder, getHomeFolderUrl
from uvc.homefolder import IHomefolders
from zope.component import getMultiAdapter, getAdapters, getUtility
from zope.dottedname.resolve import resolve
from zope.security.interfaces import IPrincipal

## def getAllProductRegistrations():
##     request = zope.security.management.getInteraction().participations[0]
##     principal = request.principal
##     return sorted(getAdapters((principal, request), IProductRegistration), key=lambda k: uvclight.order.bind().get(k[0][0]))


def getProductRegistrations():
    request = zope.security.management.getInteraction().participations[0]
    principal = request.principal
    rc = []
    for key, value in getAdapters((principal, request), IProductRegistration):
        if value.available():
            rc.append((key, value))
    return sorted(rc, key=lambda k: uvclight.order.bind().get(k[1]))


class ProductRegistration(uvclight.MultiAdapter):
    uvclight.adapts(IPrincipal, IRequest)
    uvclight.implements(IProductRegistration)
    uvclight.baseclass()
    icon = None

    def __init__(self, principal, request):
        self.principal = principal
        self.request = request
        self.title = uvclight.title.bind().get(self)
        self.name = uvclight.name.bind().get(self)
        self.description = uvclight.description.bind().get(self)

    @property
    def folderURI(self):
        if not self.productfolder:
            return
        pfn = uvclight.name.bind(get_default=default_name).get(
            self.productfolder)
        return pfn.capitalize()

    @property
    def linkname(self):
        return self.title

    @property
    def rolename(self):
        return self.title

    @property
    def productfolder(self):
        pfolder = productfolder.bind().get(self)
        if pfolder:
            return resolve(pfolder)

    def invalidRole(self):
        my_roles = uvcsite.IMyRoles(self.principal).getAllRoles()
        if not self.folderURI in my_roles:
            return True
        return False

    def available(self):
        if self.invalidRole():
            return False
        return True

    def action(self):
        try:
            home_url = getHomeFolderUrl(self.request)
            return "%s/%s/@@add" % (home_url, self.folderURI)
        except:
            return u''

    @property
    def inNav(self):
        return self.available()

    @property
    def asRole(self):
        return self.available()

    def createInProductFolder(self):
        homefolders = getUtility(IHomefolders)
        homefolder = homefolders.get(self.principal.id)
        if homefolder is None:
            homefolder = homefolders.assign_homefolder(self.principal.id)
            #utility.assignHomeFolder(uvcsite.IMasterUser(self.principal).id)

        if self.folderURI and not self.folderURI in homefolder.keys():
            pf = self.productfolder
            homefolder[self.folderURI] = pf()
            uvcsite.log('Add Productfolders %s to Homefolder: %s' % (self.folderURI, self.principal.id))
        else:
            uvcsite.log('No need for adding Folder %s to %s' % (self.folderURI, self.principal.id))


class ProductMenuItem(uvclight.Viewlet):
    uvclight.baseclass()

    def update(self):
        if hasattr(self.request, 'principal'):
            self.registration = getMultiAdapter((self.request.principal, self.request),
                IProductRegistration, self.reg_name)

    def available(self):
        return self.registration.available()

    @property
    def action(self):
        return self.registration.action()
