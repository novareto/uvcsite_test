"""
:unittest:
"""

from uvcsite import IGetHomeFolderUrl
from uvcsite.app import Uvcsite
from zope.publisher.browser import TestRequest
from zope.component import getMultiAdapter
from zope.pluggableauth import PrincipalInfo, Principal
from zope.site.hooks import getSite, setSite
from zope.app.homefolder.interfaces import IHomeFolder
import os.path
import uvcsite
import zope.app.testing.functional
import zope.security
from grok.testing import grok_component


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
                IHomeFolder(self.user),
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
