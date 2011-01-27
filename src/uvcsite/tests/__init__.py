import os.path
import uvcsite
import grok.testing

from zope.app.testing.functional import ZCMLLayer, FunctionalTestSetup
import doctest
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
