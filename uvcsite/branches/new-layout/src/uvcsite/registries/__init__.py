from z3c.baseregistry import baseregistry
import zope.component
from grokcore.component import global_utility
from zope.interface import directlyProvides
from zope.location import ILocation

name = 'something'

myRegistry = baseregistry.BaseComponents(
    zope.component.globalSiteManager, name)

directlyProvides(myRegistry, ILocation)
myRegistry.__bases__ = (myRegistry.__parent__,)

global_utility(
    myRegistry, direct=True, name=name,
    provides=zope.component.interfaces.IComponents)
