# -*- coding: utf-8 -*-

import uvclight
from ..interfaces import IUVCSite


class HAProxyCheck(uvclight.View):
    uvclight.context(IUVCSite)
    uvclight.require('zope.Public')

    def render(self):
        return "OK"
