"""
:unittest:
"""

import uvcsite
import zope.security
import zope.app.testing.functional

from uvcsite.app import Uvcsite
from uvcsite import IGetHomeFolderUrl
from uvc.homefolder.interfaces import IHomefolder

from grok.testing import grok_component
from zope.component import getMultiAdapter
from zope.site.hooks import getSite, setSite
from zope.publisher.browser import TestRequest
from zope.pluggableauth.factories import PrincipalInfo, Principal


class HomeFolderTest(zope.app.testing.functional.FunctionalTestCase):

    layer = uvcsite.tests.FunctionalLayer 

    def setUp(self):
        super(HomeFolderTest, self).setUp()
        self.user = Principal('klaus', 'klaus', 'klaus')
        self.request = TestRequest()
        self.request.setPrincipal(self.user)
        zope.security.management.newInteraction(self.request)
        root = self.getRootFolder()
        root['app'] = Uvcsite()
        setSite(root['app'])

    def tearDown(self):
        zope.security.management.endInteraction()
        super(HomeFolderTest, self).tearDown()

    def test_homefolder_instance(self):
        self.assert_(isinstance(
                IHomefolder(self.user),
                uvcsite.homefolder.homefolder.HomeFolderForPrincipal))

    def test_homefolder_url(self):
        adapter = getMultiAdapter((self.user, self.request),
                                  IGetHomeFolderUrl)
        adapter = IGetHomeFolderUrl(self.request)
        self.assertEquals('http://127.0.0.1/app/members/klaus/',
                          adapter.getURL())

    def test_add_url(self):
        adapter = IGetHomeFolderUrl(self.request)
        self.assertEquals(
            'http://127.0.0.1/app/members/klaus/adressbook/@@add',
            adapter.getAddURL(uvcsite.tests.simpleaddon.Contact))
