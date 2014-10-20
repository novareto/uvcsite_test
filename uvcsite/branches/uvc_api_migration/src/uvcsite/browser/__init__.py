# -*- coding: utf-8 -*-

import uvclight


class HAProxyCheck(uvclight.View):
    uvclight.context(uvclight.IApplication)
    uvclight.auth.require('zope.Public')

    def render(self):
        return "OK"
