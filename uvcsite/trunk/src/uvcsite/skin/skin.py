import grok
import megrok.pagelet
import megrok.resourcelibrary
from zope.interface import Interface

class IUVCSiteLayer(grok.IBrowserRequest):
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


class StandardLayout(megrok.pagelet.Layout):
    grok.context(Interface)
    megrok.pagelet.template('layout.pt')
