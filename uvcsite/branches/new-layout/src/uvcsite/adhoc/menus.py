# -*- coding: utf -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok

from uvcsite.adhoc import IAdHocLayer
from uvc.layout.slots.menus import GlobalMenu


class ADHocGlobalMenu(GlobalMenu):
    """ Globales Menu für Layer AdHoc
    """
    grok.layer(IAdHocLayer)
    grok.name('uvc.global.menu')

    def filter(self, viewlets):
        for key, value in viewlets:
            if grok.layer.bind().get(value) is IAdHocLayer:
                yield key, value
