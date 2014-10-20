# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import uvclight
import uvcsite

from ZODB.interfaces import IBroken
from hurry.workflow.interfaces import IWorkflowState
from uvc.homefolder import IHomefolder
from uvc.design.canvas import IFooterMenu
from zope.component import getUtility
from zope.interface import Interface


class StatistikMenu(uvclight.MenuItem):
    uvclight.context(uvclight.IApplication)
    uvclight.title('Statistik')
    uvclight.auth.require('zope.ManageSite')
    uvclight.menu(IFooterMenu)

    @property
    def action(self):
        return "%s/statistik" % self.view.application_url()


class StatistikView(uvclight.Page):
    uvclight.name('statistik')
    uvclight.title('Statistik')
    uvclight.auth.require('zope.ManageSite')
    uvclight.context(uvclight.IApplication)

    template = uvclight.get_template('statistikview.cpt', __file__)

    def update(self):
        self.counter = dict()
        inc = dict(anzahl=0, entwurf=0, gesendet=0, verarbeitung=0)
        #hFB = getUtility(IHomeFolderManager).homeFolderBase
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
