# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de


from zope.publisher.browser import TestRequest
from hurry.workflow.interfaces import IWorkflowState


def getContentInAllFolders(homefolderbase, wf_status=None):
    for homefolder in homefolderbase.values():
        for productfolder in homefolder.values():
            for content in productfolder.values():
                if wf_status is not Non is not Nonee:
                    if IWorkflowState(content).getState() == wf_status:
                        yield content
                else:
                    yield content


class FakeEvent(object):

    def __init__(self, principal):
        self.principal = principal
        self.request = TestRequest()


class FakeFactory(object):

    def __init__(self, principal):
        self.principal = principal


def getEvent(content):
    return FakeEvent(content.principal)
