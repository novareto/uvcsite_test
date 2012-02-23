# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import transaction
from sys import exit
from zope import component
from zope.app import homefolder

APPNAME = "app"
USERNAME = "0101010001"
OBJID = 'Entgeltnachweise'

def delObject():
    uvcsite = root[APPNAME]
    component.hooks.setSite(uvcsite)
    hfm = component.getUtility(homefolder.interfaces.IHomeFolderManager)
    for pid, productfolder in hfm.homeFolderBase.get(USERNAME).items():
        if pid == OBJID:
            del productfolder.__parent__[OBJID]
            print "Löschen des ProductFolders --> %s" % OBJID
        for id, obj in productfolder.items():
            if id == OBJID:
                del obj.__parent__[OBJID]
                print "Löschen des Objekts mit der ID --> %s" % OBJID
    transaction.commit()



if __name__ == "__main__":
    delObject()
    exit()
