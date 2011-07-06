# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite

from datetime import timedelta
from hurry.workflow.interfaces import IWorkflowState
from uvcsite.adhoc.interfaces import IAdHocFolder
from uvcsite.workflow.basic_workflow import titleForState
from zope.dublincore.interfaces import IZopeDublinCore


grok.templatedir('templates')


class Index(uvcsite.Page):
    grok.context(IAdHocFolder)

    def getValue(self, obj):
        state = IWorkflowState(obj).getState()
        if state != None:
            return titleForState(state)
        return self.defaultValue

    @property
    def getObject(self):
        obj = self.context.get(self.request.principal.title)
        if obj:
            return dict(
                    title = obj.title,
                    datum = (IZopeDublinCore(obj).modified + timedelta(hours=2)).strftime('%d.%m.%Y %H:%M'),
                    status = self.getValue(obj)) 
