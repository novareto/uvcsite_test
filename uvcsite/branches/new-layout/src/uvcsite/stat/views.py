# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from hurry.workflow.interfaces import IWorkflowState

from zope.component import getUtility
from zope.app.homefolder.interfaces import IHomeFolderManager


grok.templatedir('templates')


class StatistikView(uvcsite.Page):
    grok.name('statistik')
    grok.title('Statistik')
    grok.require('zope.ManageSite')

    grok.context(uvcsite.IUVCSite)
    #uvcsite.menu(uvcsite.Footer, order=200)

    def update(self):
        self.counter = dict()
        inc = dict(anzahl=0, entwurf=0, gesendet=0)
        hFB = getUtility(IHomeFolderManager).homeFolderBase
        self.counter['HomeFolder'] = inc
        self.counter['HomeFolder']['anzahl'] = len(hFB)
        for homefolder in hFB.values():
            for name, pf in homefolder.items():
                if name not in self.counter:
                    self.counter[name] = dict(anzahl=0, entwurf=0, gesendet=0) 
                self.counter[name]['anzahl'] += len(pf)
                for obj in pf.values():
                    if IWorkflowState(obj).getState() == 0:
                        self.counter[name]['entwurf'] += 1 
                    elif IWorkflowState(obj).getState() == 1:
                        self.counter[name]['gesendet'] += 1 
