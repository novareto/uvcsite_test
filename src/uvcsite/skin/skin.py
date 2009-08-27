# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout
import megrok.resourcelibrary

from zope.interface import Interface
from megrok.z3cform.skin import FormLayer, TableLayer


class IUVCSiteLayer(FormLayer):
    pass


class IUVCSiteSkin(IUVCSiteLayer, grok.IDefaultBrowserLayer):
    grok.skin('uvcsiteskin')


class Styles(megrok.resourcelibrary.ResourceLibrary):
    grok.name('uvcresources')
    grok.layer(IUVCSiteLayer)
    megrok.resourcelibrary.directory('styles')
    megrok.resourcelibrary.include('main.css')
    megrok.resourcelibrary.include('nva.css')


class Scripts(megrok.resourcelibrary.ResourceLibrary):
    grok.name('uvcscripts')
    grok.layer(IUVCSiteLayer)
    megrok.resourcelibrary.directory('javascripts')
    megrok.resourcelibrary.include('jquery-1.3.2.js')
    megrok.resourcelibrary.include('jtip.js')
    megrok.resourcelibrary.include('myjs.js')
    megrok.resourcelibrary.include('jquery.tablesorter.js')
    megrok.resourcelibrary.include('mytable.js')
    megrok.resourcelibrary.include('jquery-ui-1.7.2.custom.min.js')


class StandardLayout(megrok.layout.Layout):
    grok.context(Interface)
