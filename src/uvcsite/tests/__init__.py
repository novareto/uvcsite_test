import os.path
import uvcsite
import grok.testing

from zope.app.testing.functional import ZCMLLayer, FunctionalTestSetup
from zope.testing import doctest
from pkg_resources import resource_listdir
import unittest
import sys


product_config = """ 
 <product-config mailer>
    queue-path /tmp/mailer-queue
    hostname localhost
    port 25
#    username
#    password
 </product-config>
"""


ftesting_zcml = os.path.join(
    os.path.dirname(uvcsite.__file__), 'ftesting_uvc.zcml')
FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer',
                            allow_teardown=True, product_config=product_config)


def setUp(test):
    FunctionalTestSetup().setUp()
    if getattr(sys.modules[test.name], '__grok__', True):
        grok.testing.grok(test.name)


def tearDown(test):
    FunctionalTestSetup().tearDown()


def suiteFromPackage(name):
    files = resource_listdir(name.split('.')[0], '/'.join(name.split('.')[1:]))
    suite = unittest.TestSuite()
    for filename in files:
        if not filename.endswith('.py'):
            continue
        if filename == '__init__.py':
            continue

        dottedname = '%s.%s' % (name, filename[:-3])
        test = doctest.DocTestSuite(
            dottedname, setUp=setUp, tearDown=tearDown,
            optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
        test.layer = FunctionalLayer
        suite.addTest(test)
    return suite
