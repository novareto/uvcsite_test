# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import six
import doctest
import uvcsite
import os.path
import re
import unittest
import zope.app.appsetup
import zope.app.wsgi.testlayer
import zope.testbrowser.wsgi
import zope.i18n
import zope.i18n.config

from cStringIO import StringIO
from pkg_resources import resource_listdir
from zope.testing import renormalizing
from zope.app.wsgi.testlayer import http
from grokcore.xmlrpc.ftests.test_grok_functional import XMLRPCTestTransport




class Layer(zope.testbrowser.wsgi.TestBrowserLayer,
            zope.app.wsgi.testlayer.BrowserLayer):

    product_config = u"""
        <product-config mailer>
            queue-path /tmp/mailer-queue
            hostname localhost
            port 25
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

    def __init__(self, *args, **kw):
        config = zope.app.appsetup.product.loadConfiguration(
            StringIO(self.product_config))
        self.conf = [
            zope.app.appsetup.product.FauxConfiguration(name, values)
            for name, values in config.items()]
        zope.testbrowser.wsgi.TestBrowserLayer.__init__(self)
        zope.app.wsgi.testlayer.BrowserLayer.__init__(self, *args, **kw)

    def setUp(self):
        zope.app.appsetup.product.setProductConfigurations(self.conf)
        zope.app.wsgi.testlayer.BrowserLayer.setUp(self)
        old_1, old_2 = zope.i18n.negotiate, zope.i18n.config.ALLOWED_LANGUAGES
        zope.i18n.negotiate = lambda context: 'de'
        zope.i18n.config.ALLOWED_LANGUAGES = ['de']


layer = Layer(uvcsite, allowTearDown=True)


checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:'),
    ])


def http_call(app, method, path, data=None, **kw):
    """Function to help make RESTful calls.

    method - HTTP method to use
    path - testbrowser style path
    data - (body) data to submit
    kw - any request parameters
    """

    if path.startswith('http://localhost'):
        path = path[len('http://localhost'):]
    request_string = '%s %s HTTP/1.1\n' % (method, path)
    for key, value in kw.items():
        request_string += '%s: %s\n' % (key, value)
    if data is not None:
        request_string += 'Content-Length:%s\n' % len(data)
        request_string += '\r\n'
        request_string += data
    if six.PY3:
        request_string = request_string.encode()
    return http(app, str(request_string), handle_errors=False)


def suiteFromPackage(name):
    layer_dir = 'functional'
    files = resource_listdir(__name__, '{}/{}'.format(layer_dir, name))
    suite = unittest.TestSuite()
    getRootFolder = layer.getRootFolder
    transport = XMLRPCTestTransport()
    transport.wsgi_app = layer.make_wsgi_app
    
    globs = dict(
        __name__='uvcsite',
        getRootFolder=getRootFolder,
        http=zope.app.wsgi.testlayer.http,
        http_call=http_call,
        wsgi_app=layer.make_wsgi_app,
        transport=transport,
        )

    optionflags = (
        renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2 +
        doctest.IGNORE_EXCEPTION_DETAIL +
        doctest.ELLIPSIS +
        doctest.NORMALIZE_WHITESPACE +
        doctest.REPORT_NDIFF
        )
    
    extraglobs = {'unicode_literals': unicode_literals}
    doctest.testmod(extraglobs=extraglobs)

    for filename in files:
        if filename == '__init__.py':
            continue

        test = None
        if filename.endswith('.py'):
            dottedname = 'uvcsite.tests.%s.%s.%s' % (
                layer_dir, name, filename[:-3])
            test = doctest.DocTestSuite(
                dottedname,
                checker=checker,
                extraglobs=globs,
                optionflags=optionflags)
        elif filename.endswith('.txt'):
            test = doctest.DocFileSuite(
                os.path.join(layer_dir, name, filename),
                optionflags=optionflags,
                globs=globs)
        if test is not None:
            test.layer = layer
            suite.addTest(test)
    return suite


def test_suite():
    suite = unittest.TestSuite()
    for name in (
            "auth",
            "base",
            "content",
            "extranetmembership",
            "homefolder",
            "stat",
            "utils",
            "viewlets",
            "workflow",
            "cataloging",
            "plugins"):
        suite.addTest(suiteFromPackage(name))
    return suite
