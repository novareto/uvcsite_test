# -*- coding: utf-8 -*-

from cromlech.browser import exceptions
from uvclight import get_template, Page
from grokcore.component import name, context, implements
from grokcore.security import require
from zope.location import locate, LocationProxy


class UnauthorizedPage(Page):
    name('')
    context(exceptions.HTTPUnauthorized)
    require('zope.Public')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self):
        return (u"This page is protected and you're not allowed."
                u" Please login.")

    
class ForbiddenPage(Page):
    name('')
    context(exceptions.HTTPForbidden)
    require('zope.Public')

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self):
        return u"This page is protected and you don't have the credentials."
