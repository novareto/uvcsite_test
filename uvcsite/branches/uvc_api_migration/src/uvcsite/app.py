# -*- coding: utf-8 -*-

import uvclight

from .interfaces import IUVCSite

from webob.dec import wsgify

from grokcore.component import global_utility
from grokcore.registries import create_components_registry

from cromlech.browser import IPublicationRoot
from cromlech.browser import PublicationBeginsEvent, PublicationEndsEvent
from cromlech.configuration.utils import load_zcml
from cromlech.dawnlight import DawnlightPublisher
from cromlech.dawnlight import ViewLookup
from cromlech.dawnlight import view_locator, query_view
from cromlech.dawnlight.directives import traversable
from cromlech.i18n import register_allowed_languages
from cromlech.security import Interaction
from cromlech.webob.request import Request
from cromlech.zodb import Site, PossibleSite, get_site
from cromlech.zodb.components import LocalSiteManager
from cromlech.zodb.middleware import ZODBApp
from cromlech.zodb.utils import init_db
from dolmen.container.components import BTreeContainer
from transaction import manager as transaction_manager
from zope.component import globalSiteManager
from zope.component.interfaces import IComponents
from zope.component.interfaces import ISite, IPossibleSite
from zope.event import notify
from zope.interface import implementer
from zope.location import Location
from zope.security.proxy import removeSecurityProxy
from uvclight import sessionned
from uvclight.auth import Principal
from .auth.handler import USERS

# this is to test
from uvc.themes.dguv import IDGUVRequest
from zope.interface import alsoProvides


uvcsiteRegistry = create_components_registry(
    name="uvcsiteRegistry",
    bases=tuple(),
)


global_utility(
    uvcsiteRegistry,
    name="uvcsiteRegistry",
    provides=IComponents,
    direct=True)


@implementer(IPublicationRoot, IUVCSite)
class UVCSite(BTreeContainer, PossibleSite, Location):
    traversable('members')

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


view_lookup = ViewLookup(view_locator(query_view))

    
class UVCApplication(object):

    def __init__(self, environ_key, name):
        self.environ_key = environ_key
        self.name = name
        self.publisher = DawnlightPublisher(view_lookup=view_lookup)

    def __call__(self, environ, start_response):
        conn = environ[self.environ_key]
        site = get_site(conn, self.name)

        @uvclight.sessionned('session.key')
        @uvclight.auth.secured(USERS, u"Please Login")
        def publish(environ, start_response):
            with uvclight.Request(environ) as request:
                alsoProvides(request, IDGUVRequest)
                principal = request.principal = uvclight.Principal(
                    environ['REMOTE_USER'])
            
                with Site(site):
                    with Interaction(principal):
                        notify(PublicationBeginsEvent(self, request))
                        response = removeSecurityProxy(self.publisher.publish(
                            request, site, handle_errors=True))
                        notify(PublicationEndsEvent(request, response))

            return response(environ, start_response)

        return publish(environ, start_response)
        

def make_application(model, name):
    def create_app(db):
        conn = db.open()
        try:
            root = conn.root()
            if not name in root:
                with transaction_manager:
                    application = root[name] = model()
                    if (not ISite.providedBy(application) and
                        IPossibleSite.providedBy(application)):
                        LocalSiteManager(application)
        finally:
            conn.close()
    return create_app


def uvcsite(global_conf, configuration, zcml_file, env_key, app_key):
    load_zcml(zcml_file)
    register_allowed_languages(['de', 'de-de'])
    db = init_db(configuration, make_application(UVCSite, app_key))
    app = UVCApplication(env_key, app_key)
    return ZODBApp(app, db, key=env_key)
