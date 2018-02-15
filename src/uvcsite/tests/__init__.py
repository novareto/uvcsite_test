# -*- coding: utf-8 -*-

from zope.security import management
from zope.publisher.browser import TestRequest
from zope.pluggableauth.factories import Principal


def startInteraction(principal, request=None):
    if not request:
        request = TestRequest()
    request.setPrincipal(Principal(principal, principal))
    management.newInteraction(request)
    return request


def endInteraction():
    management.endInteraction()
