# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import os.path
import transaction
import unittest2
import uvcsite
import zope.app.appsetup
import zope.app.wsgi.testlayer
import zope.component.testlayer
import zope.security

from StringIO import StringIO
from uvcsite.app import Uvcsite
from zope.site.hooks import setSite
from zope.app.testing.functional import ZCMLLayer
from zope.publisher.browser import TestRequest
from zope.pluggableauth.factories import Principal


class TestCase(unittest2.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.getRootFolder = self.layer.getRootFolder
        self.app = self.layer.getRootFolder()['app']


product_config = """
 <product-config mailer>
    queue-path /tmp/mailer-queue
    hostname localhost
    port 25
#    username
#    password
 </product-config>
 <product-config beaker>
   session.type            cookie
   session.data_dir
   session.lock_dir        /tmp/sessions/lock
   session.key             beaker.session.id
   session.secret          secret
   session.validatekey     fdjaksfj
 </product-config>

"""


ftesting_zcml = os.path.join(
    os.path.dirname(uvcsite.__file__),
    'ftesting_uvc.zcml',
)


FunctionalLayer = ZCMLLayer(
    ftesting_zcml, __name__,
    'FunctionalLayer',
    allow_teardown=True,
    product_config=product_config,
)


class BaseUVCBrowserLayer(zope.app.wsgi.testlayer.BrowserLayer):

    def __init__(self, *args, **kw):
        self.conf = zope.app.appsetup.product.loadConfiguration(
            StringIO(kw.pop('product_config', '')))
        self.conf = [
            zope.app.appsetup.product.FauxConfiguration(name, values)
            for name, values in self.conf.items()]
        #super(BaseUVCBrowserLayer, self).__init__(*args, **kw)
        zope.app.wsgi.testlayer.BrowserLayer.__init__(self, *args, **kw)
        zope.component.testlayer.ZCMLFileLayer.__init__(self, *args, **kw)

    def setUp(self):
        zope.app.appsetup.product.setProductConfigurations(self.conf)
        zope.app.wsgi.testlayer.BrowserLayer.setUp(self)
        root = self.getRootFolder()
        root['app'] = Uvcsite()
        setSite(root['app'])
        transaction.commit()


UVCBrowserLayer = BaseUVCBrowserLayer(
    uvcsite,
    zcml_file='ftesting_uvc.zcml',
    product_config=product_config,
)


def startInteraction(principal, request=None):
    if not request:
        request = TestRequest()
    request.setPrincipal(Principal(principal, principal))
    zope.security.management.newInteraction(request)
    return request


def endInteraction():
    zope.security.management.endInteraction()


#
## Example for SELENIUM BASED Tests
#

#class SeleniumProductConfigLayer(gocept.selenium.grok.Layer):
#    """ """
#
#    def __init__(self, *args, **kw):
#        self.conf = zope.app.appsetup.product.loadConfiguration(
#            StringIO(kw.pop('product_config', '')))
#        self.conf = [
#            zope.app.appsetup.product.FauxConfiguration(name, values)
#            for name, values in self.conf.items()]
#        gocept.selenium.grok.Layer.__init__(self, *args, **kw)
#
#    def setUp(self):
#        zope.app.appsetup.product.setProductConfigurations(self.conf)
#        gocept.selenium.grok.Layer.setUp(self)
#        root = self.getRootFolder()
#        root['app'] = Uvcsite()
#        transaction.commit()


#SeleniumLayer = SeleniumProductConfigLayer(
#    uvcsite,
#    zcml_file='ftesting_uvc.zcml',
#    product_config=product_config,
#    )
