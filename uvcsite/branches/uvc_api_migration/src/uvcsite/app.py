# -*- coding: utf-8 -*-

import uvclight
from uvclight import publishing, auth
from uvclight.backends import zodb

from grokcore.registries import create_components_registry
from cromlech.i18n import register_allowed_languages
from cromlech.webob.request import Request
from cromlech.zodb import Site, get_site

from cromlech.zodb.middleware import ZODBApp
from cromlech.zodb.utils import init_db
from cromlech.security import unauthenticated_principal
from zope.component import globalSiteManager
from zope.component.interfaces import IComponents
from zope.event import notify
from zope.security.management import setSecurityPolicy
from zope.security.proxy import removeSecurityProxy
from zope.securitypolicy.zopepolicy import ZopeSecurityPolicy

# this is to test
from .auth.handler import USERS
from uvc.themes.dguv import IDGUVRequest
from zope.interface import alsoProvides


uvcsiteRegistry = create_components_registry(
    name="uvcsiteRegistry",
    bases=tuple(),
    )


uvclight.global_utility(
    uvcsiteRegistry,
    name="uvcsiteRegistry",
    provides=IComponents,
    direct=True,
    )


@uvclight.implementer(uvclight.IApplication)
class UVCSite(zodb.Root):
    uvclight.traversable('members')

    def getSiteManager(self):
        current = super(UVCSite, self).getSiteManager()
        if uvcsiteRegistry not in current.__bases__:
            uvcsiteRegistry.__bases__ = tuple(
                [x for x in uvcsiteRegistry.__bases__
                    if x._hash_() != globalSiteManager._hash_()])
            current.__bases__ = (uvcsiteRegistry,) + current.__bases__
        elif current.__bases__[0] is not uvcsiteRegistry:
            current.__bases__ = (uvcsiteRegistry,) + tuple((
                b for b in current.__bases__ if b != uvcsiteRegistry))
        return current


class UVCApplication(object):

    def __init__(self, environ_key, name, session_key):
        self.environ_key = environ_key
        self.name = name
        self.publisher = publishing.create_base_publisher(secure=True)
        self.session_key = session_key

    def __call__(self, environ, start_response):
        request = Request(environ)
        alsoProvides(request, IDGUVRequest)
        uvclight.setRequest(request)

        @uvclight.sessionned(self.session_key)
        def publish(environ, start_response):
            user = environ.get('REMOTE_USER')
            if user is not None:
                request.principal = uvclight.Principal(user)
            else:
                request.principal = unauthenticated_principal
            with uvclight.Interaction(request.principal):
                notify(uvclight.PublicationBeginsEvent(self, request))
                response = removeSecurityProxy(
                    self.publisher.publish(request, site, handle_errors=True))
                notify(uvclight.PublicationEndsEvent(request, response))
                return response(environ, start_response)

        conn = environ[self.environ_key]
        site = get_site(conn, self.name)
        with Site(site):
            return publish(environ, start_response)


def uvcsite(gconf, configuration, zcml_file, session_key, env_key, app_key):
    setSecurityPolicy(auth.SimpleSecurityPolicy)
    uvclight.load_zcml(zcml_file)
    register_allowed_languages(['de', 'de-de'])
    db = init_db(configuration, zodb.make_application(app_key, UVCSite))
    app = UVCApplication(env_key, app_key, session_key)
    return ZODBApp(app, db, key=env_key)
