# -*- coding: utf -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok

from uvc.layout.layout import IUVCLayer


class IAdHocLayer(IUVCLayer):
    """ Layer for AdHoc
    """
    pass


class AdHocLayer(IAdHocLayer):
    """ Skin For ADHoc
    """
    grok.skin('adhoc')
