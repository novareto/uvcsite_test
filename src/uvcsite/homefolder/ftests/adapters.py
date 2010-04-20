"""
:unittest:
"""

from uvcsite import IGetHomeFolderUrl
from uvcsite.app import Uvcsite
from zope.publisher.browser import TestRequest
from zope.component import getMultiAdapter
from zope.app.authentication.principalfolder import PrincipalInfo, Principal
from zope.app.component.hooks import getSite, setSite
from zope.app.homefolder.interfaces import IHomeFolder
import os.path
import uvcsite
import zope.app.testing.functional


zope.app.testing.functional.defineLayer('ftesting', '../../ftesting.zcml')


class HomeFolderTest(zope.app.testing.functional.FunctionalTestCase):

    layer = ftesting

    def setUp(self):
        super(HomeFolderTest, self).setUp()
        self.user = Principal('klaus', 'klaus', 'klaus')
        root = self.getRootFolder()
        root['app'] = Uvcsite()
        setSite(root['app'])

    def test_homefolder_instance(self):
        self.assert_(isinstance(
                IHomeFolder(self.user),
                uvcsite.homefolder.homefolder.HomeFolderForPrincipal))

    def test_homefolder_url(self):
        request = TestRequest()
        adapter = getMultiAdapter((self.user, request), IGetHomeFolderUrl)
        self.assertEquals('http://127.0.0.1/app/members/klaus/',
                          adapter.getURL())
