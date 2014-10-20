# -*- coding: utf-8 -*-

from uvc.homefolder.components import Homefolders
from uvc.homefolder.interfaces import IHomefolders
from uvclight import subscribe, IApplicationInitializedEvent
from zope.component.interfaces import ISite
from zope.interface import Interface
from ..app import UVCSite


@subscribe(UVCSite, IApplicationInitializedEvent)
def register_homefolders(site, event):
    homefolders = site['homefolders'] = Homefolders()
    sm = site.getSiteManager()
    sm.registerUtility(homefolders, IHomefolders)
