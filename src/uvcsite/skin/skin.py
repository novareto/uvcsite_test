import grok
import megrok.layout
import megrok.resourcelibrary

from zope.interface import Interface
from megrok.z3cform.skin import FormLayer, TableLayer


class IUVCSiteLayer(FormLayer):
    pass


class IUVCSiteSkin(IUVCSiteLayer, grok.IDefaultBrowserLayer):
    grok.skin('uvcsiteskin')


class Resources(megrok.resourcelibrary.ResourceLibrary):
    """ Resourcen for uvcsite"""
    grok.name('uvcresources')
    grok.layer(IUVCSiteLayer)
    megrok.resourcelibrary.directory('resources')
    megrok.resourcelibrary.include('jquery-1.3.2.js')
    megrok.resourcelibrary.include('jtip.js')
    megrok.resourcelibrary.include('myjs.js')
    megrok.resourcelibrary.include('jquery.tablesorter.js')
    megrok.resourcelibrary.include('mytable.js')
    megrok.resourcelibrary.include('tooltip.css')
    megrok.resourcelibrary.include('tableform.css')
    megrok.resourcelibrary.include('worldcookery.css')

class StandardLayout(megrok.layout.Layout):
    grok.context(Interface)
