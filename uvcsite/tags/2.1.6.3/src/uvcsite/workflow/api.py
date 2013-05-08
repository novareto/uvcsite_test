# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from hurry.workflow.interfaces import IWorkflowInfo, IWorkflowState


class WorkflowAPI(grok.XMLRPC):
    grok.context(uvcsite.IContent)

    def publish(self):
        return IWorkflowInfo(self.context).fireTransition('publish')

    def progress(self):
        return IWorkflowInfo(self.context).fireTransition('progress')

    def fix(self):
        return IWorkflowInfo(self.context).fireTransition('fix')

    def state(self):
        return IWorkflowState(self.context).getState()
