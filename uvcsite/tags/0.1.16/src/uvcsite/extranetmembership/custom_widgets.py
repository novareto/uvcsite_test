# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import grok

from z3c.form import interfaces
from megrok.z3cform.base import WidgetTemplate, directives 
from uvcsite.extranetmembership.enms import ENMSUpdateUser#, ENMSCreateUser
#from uvcsite.interfaces import IMyHomeFolder
#import zope.schema.interfaces
from zope.interface import Interface
from uvc.skin.skin import IUVCSkin

class CustomPasswordWidget(WidgetTemplate):
    grok.context(Interface)
    grok.layer(IUVCSkin)
    grok.view(ENMSUpdateUser)
    directives.widget(interfaces.IPasswordWidget)
    directives.mode(interfaces.INPUT_MODE)
    grok.template('templates/password.pt')


#class CustomInputWidgetU(WidgetTemplate):
#    grok.context(Interface)
#    grok.layer(IUVCSkin)
#    grok.view(ENMSUpdateUser)
#    directives.widget(interfaces.ITextWidget)
#    directives.mode(interfaces.INPUT_MODE)
#    grok.template('templates/input_hidden_span.pt')
#
#
#class CustomInputWidgetA(WidgetTemplate):
#    grok.context(Interface)
#    grok.layer(IUVCSkin)
#    grok.view(ENMSCreateUser)
#    directives.widget(interfaces.ITextWidget)
#    directives.mode(interfaces.INPUT_MODE)
#    grok.template('templates/input_hidden_span.pt')
