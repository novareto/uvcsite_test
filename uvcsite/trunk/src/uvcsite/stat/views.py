# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from hurry.workflow.interfaces import IWorkflowState

from zope.component import getUtility
from zope.app.homefolder.interfaces import IHomeFolderManager
from ZODB.interfaces import IBroken


grok.templatedir('templates')


class StatistikView(uvcsite.Page):
    grok.name('statistik')
    grok.title('Statistik')
    grok.require('zope.ManageSite')

    grok.context(uvcsite.IUVCSite)
    uvcsite.menu(uvcsite.IFooter, order=200)

    def update(self):
        self.counter = dict()
        inc = dict(anzahl=0, entwurf=0, gesendet=0, verarbeitung=0)
        hFB = getUtility(IHomeFolderManager).homeFolderBase
        self.counter['HomeFolder'] = inc
        self.counter['HomeFolder']['anzahl'] = len(hFB)
        pf_c = 0
        for homefolder in hFB.values():
            for name, pf in homefolder.items():
                if not IBroken.providedBy(pf):
                    pf_c += 1
                    if name not in self.counter:
                        self.counter[name] = dict(anzahl=0, entwurf=0, gesendet=0, verarbeitung=0) 
                    self.counter[name]['anzahl'] += len(pf)
                    for obj in pf.values():
                        state = IWorkflowState(obj).getState()
                        if state == 0:
                            self.counter[name]['entwurf'] += 1 
                        elif state == 1:
                            self.counter[name]['gesendet'] += 1 
                        elif state == 2:
                            self.counter[name]['verarbeitung'] += 1 
        self.counter['ProductFolders'] = dict() 
        self.counter['ProductFolders']['anzahl'] = pf_c
