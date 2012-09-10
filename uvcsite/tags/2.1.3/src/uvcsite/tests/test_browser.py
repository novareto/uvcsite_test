import unittest
import transaction
import uvcsite.tests
import datetime

from megrok.layout import ILayout
from mock import Mock
from uvcsite.app import Uvcsite, CustomDateFieldWidget
from zeam.form.base import Form
from zope import component
from zope import interface, component
from zope.authentication.interfaces import IAuthentication
from zope.pluggableauth.authentication import PluggableAuthentication
from zope.publisher.browser import TestRequest
from zope.publisher.browser import applySkin
from zope.testbrowser.wsgi import Browser


class ApplicationTests(uvcsite.tests.TestCase):

    layer = uvcsite.tests.UVCBrowserLayer

    def test_known_application(self):
        root = self.getRootFolder()
        app = root['app']
        self.assertIsInstance(app, Uvcsite)


    def test_authentication_infrastucture(self):
        auth_util = component.getUtility(IAuthentication)
        self.assertIsInstance(auth_util, PluggableAuthentication)

    def test_bla(self):
        browser = Browser()


class ZeamFormOverridesTests(unittest.TestCase):

    def test_zeam_widget_extraction(self):
        pass

    def test_custom_date_field_widget(self):
        obj = Mock()
        obj.prefix = "objprefix"
        obj.identifier= "objident"
        request = TestRequest()
        form = Form(obj, request)
        form.prefix="form.prefix"
        datefield = CustomDateFieldWidget(obj, form, request)
        datum = datetime.date(2011,01,01)
        self.assertEqual(datefield.valueToUnicode(datum), u'2011 1 1 ')
        
