import grok
import megrok.layout
import megrok.resourcelibrary

from zope.interface import Interface
from megrok.z3cform.skin import FormLayer


class IUVCSiteLayer(FormLayer):
    pass


class IUVCSiteSkin(IUVCSiteLayer, grok.IDefaultBrowserLayer):
    grok.skin('uvcsiteskin')


class Resources(megrok.resourcelibrary.ResourceLibrary):
    """ Resourcen for uvcsite"""
    grok.name('uvcresources')
    grok.layer(IUVCSiteLayer)
    #grok.require('uvc.Member')
    megrok.resourcelibrary.directory('resources')
    megrok.resourcelibrary.include('worldcookery.css')
    megrok.resourcelibrary.include('jquery-1.3.2.js')
    megrok.resourcelibrary.include('jtip.js')
    megrok.resourcelibrary.include('myjs.js')
    megrok.resourcelibrary.include('tooltip.css')


class StandardLayout(megrok.layout.Layout):
    grok.context(Interface)
