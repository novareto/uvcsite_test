# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import zope.component.interfaces


from zope import interface


class IAfterSaveEvent(zope.component.interfaces.IObjectEvent):
    "My special event"

    principal = interface.Attribute("Pincipal")


class AfterSaveEvent(zope.component.interfaces.ObjectEvent):
    grok.implements(IAfterSaveEvent)

    def __init__(self, object, principal):
        self.object = object
        self.principal = principal
