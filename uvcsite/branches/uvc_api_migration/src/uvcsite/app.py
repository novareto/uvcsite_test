# -*- coding: utf-8 -*-

import uvclight
import ConfigParser, os

from uvclight import publishing, auth
from uvclight.context import ContextualRequest
from uvclight.backends import zodb

from grokcore.registries import create_components_registry
from cromlech.i18n import register_allowed_languages
from cromlech.webob.request import Request
from cromlech.zodb import Site, get_site
from cromlech.zodb.middleware import ZODBApp
from cromlech.zodb.utils import init_db
from cromlech.browser import getSession
from cromlech.security import unauthenticated_principal
from zope.component import globalSiteManager
from zope.component.interfaces import IComponents
from zope.event import notify
from zope.security.management import setSecurityPolicy
from zope.security.proxy import removeSecurityProxy
from zope.securitypolicy.zopepolicy import ZopeSecurityPolicy
from zope.annotation.interfaces import IAttributeAnnotatable


# this is to test
from . import log
from .auth.handler import USERS
from .utils.mail import configure_mail
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


@uvclight.implementer(IAttributeAnnotatable)
@uvclight.implementer(uvclight.IApplication)
class UVCSite(zodb.Root):
    uvclight.traversable('members')
    credentials = ['simple']

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
        self.publish = publishing.create_base_publisher(secure=True).publish
        self.session_key = session_key

    def __call__(self, environ, start_response):

        @uvclight.sessionned(self.session_key)
        def publish(environ, start_response):
            with ContextualRequest(environ, layers=[IDGUVRequest]) as request:
                session = getSession()
                user = environ.get('REMOTE_USER') or session.get('username')
                if user:

                    request.principal = uvclight.auth.Principal(user)
                    print request.principal
                else:
                    request.principal = unauthenticated_principal

                conn = environ[self.environ_key]
                site = get_site(conn, self.name)
                with Site(site):
                    with uvclight.Interaction(request.principal):
                        response = self.publish(request, site)
                        response = removeSecurityProxy(response)
                        return response(environ, start_response)

        return publish(environ, start_response)


def configure(config_file, app):
    with open(config_file, 'r') as fd:
        config = ConfigParser.ConfigParser()
        config.readfp(fd)

    for section in config.sections():
        items = dict(config.items(section))
        loader = items.pop('use')
        if loader is not None:
            func = uvclight.eval_loader(loader)
            func(items, app)
            log(u'Loaded configuration for %r.' % section)
        else:
            log(u'Unable to load configuration for %r, `use` is missing.'
                % section)


def uvcsite(gconf, zodb_conf, zcml_file, session_key, env_key, app_key, **kws):
    setSecurityPolicy(auth.SimpleSecurityPolicy)
    uvclight.load_zcml(zcml_file)
    register_allowed_languages(['de', 'de-de'])
    db = init_db(zodb_conf, zodb.make_application(app_key, UVCSite))
    app = UVCApplication(env_key, app_key, session_key)

    config_file = kws.get('conf_file')
    if config_file is not None:
        configure(config_file, app)

    return ZODBApp(app, db, key=env_key)
