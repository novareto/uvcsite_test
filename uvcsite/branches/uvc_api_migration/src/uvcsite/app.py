# -*- coding: utf-8 -*-

import uvclight
import ConfigParser, os

from uvclight import auth
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


@uvclight.implementer(uvclight.IApplication, IAttributeAnnotatable)
class UVCSite(zodb.Root):
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


class UVCApplication(zodb.ZODBPublication, auth.SecurePublication):

    layers = [IDGUVRequest]

    def principal_factory(self, username):
        if username:
            return auth.Principal(user, permissions=set(('zope.View',)))
        return unauthenticated_principal



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
    setSecurityPolicy(auth.GenericSecurityPolicy)
    app = UVCApplication.create(
        gconf,
        session_key=session_key,
        environ_key=env_key,
        conf=zodb_conf,
        zcml_file=zcml_file,
        name=app_key,
        root=UVCSite,
        **kws)

    config_file = kws.get('conf_file')
    if config_file is not None:
        configure(config_file, app)

    return app
