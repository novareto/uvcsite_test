from z3c.baseregistry import baseregistry
import zope.component
from grokcore.component import global_utility
from zope.interface import directlyProvides
from zope.location import ILocation


class SimpleRegistry(baseregistry.BaseComponents):
    pass


def register_registry(name, factory):
    myRegistry = factory(zope.component.globalSiteManager, name)
    directlyProvides(myRegistry, ILocation)
    myRegistry.__bases__ = (myRegistry.__parent__,)
    gsm = zope.component.getGlobalSiteManager()
    gsm.registerUtility(myRegistry, zope.component.interfaces.IComponents, name=name)


def load(loader_entry):
    module, expr = loader_entry.split(':', 1)
    if module:
        d = __import__(module, {}, {}, ['*']).__dict__
    else:
        d={}
    return eval(expr, d)


def provide_registries(app, global_conf, **registries):
    for key, value in registries.items():
        factory = load(value)
        register_registry(key, factory)
    return app
