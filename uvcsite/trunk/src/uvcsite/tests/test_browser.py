import unittest
import uvcsite.tests

from zope import interface, component
from uvcsite.app import Uvcsite
from zope.publisher.browser import applySkin
from megrok.layout import ILayout
from uvcsite.mobile import MobileLayer
from zope.publisher.browser import TestRequest
import transaction
from zope.testbrowser.wsgi import Browser
from zope.authentication.interfaces import IAuthentication
from zope import component
from zope.pluggableauth.authentication import PluggableAuthentication


class ApplicationTests(uvcsite.tests.TestCase):

    layer = uvcsite.tests.UVCBrowserLayer

    def test_known_application(self):
        root = self.getRootFolder()
        app = root['app']
        self.assertIsInstance(app, Uvcsite)


    def test_authentication_infrastucture(self):
        auth_util = self.app._sm.getUtility(IAuthentication)
        self.assertIsInstance(auth_util, PluggableAuthentication)

    def test_bla(self):
        browser = Browser()
