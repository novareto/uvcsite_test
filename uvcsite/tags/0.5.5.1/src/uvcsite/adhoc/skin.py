# -*- coding: utf -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
from interfaces import IAdHocLayer

class AdHocLayer(IAdHocLayer):
    """ Skin For ADHoc
    """
    grok.skin('adhoc')
