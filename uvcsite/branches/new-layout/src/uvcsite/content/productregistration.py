# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite
import zope.security

from zope.security.interfaces import IPrincipal
from zope.publisher.interfaces.http import IHTTPRequest
from uvcsite.content.interfaces import IProductRegistration
from uvcsite.content.directive import productfolder
from zope.dottedname.resolve import resolve
from zope.component import getMultiAdapter, getAdapters, getUtility
from zope.app.homefolder.interfaces import IHomeFolderManager
from uvcsite.content.meta import default_name


def getProductRegistrations():
    request = zope.security.management.getInteraction().participations[0] 
    principal = request.principal
    return dict(getAdapters((principal, request), IProductRegistration))


class ProductRegistration(grok.MultiAdapter):
    grok.adapts(IPrincipal, IHTTPRequest)
    grok.implements(IProductRegistration)
    grok.baseclass()
    icon = None

    def __init__(self, principal, request):
        self.principal = principal
        self.request = request
        self.title = grok.title.bind().get(self)
        self.name = grok.name.bind().get(self)

    @property
    def folderURI(self):
        grok.name.bind(get_default=default_name).get(self.productfolder)
        return self.name.capitalize()

    @property
    def linkname(self):
        return self.title

    @property
    def rolename(self):
        return self.title

    @property
    def productfolder(self):
        return resolve(productfolder.bind().get(self))

    def available(self):
        return True

    def action(self):
        return "%s/%s/@@add" % (uvcsite.getHomeFolderUrl(self.request), self.folderURI)

    def createInProductFolder(self):
        homefolder = uvcsite.getHomeFolder(self.request)
        if not homefolder:
            utility = getUtility(IHomeFolderManager)
            utility.assignHomeFolder(uvcsite.IMasterUser(self.request.principal).id)
        if not self.folderURI in homefolder.keys():
            pf = self.productfolder
            homefolder[self.folderURI] = pf() 
        else:
            print "FOLDER %s ---> already there" % self.folderURI


class ProductMenuItem(uvcsite.MenuItem):
    grok.baseclass()

    def update(self):
        self.registration = getMultiAdapter((self.request.principal, self.request),
            IProductRegistration, self.reg_name)

    def available(self):
        return self.registration.available()

    @property
    def action(self):
        return self.registration.action()
