# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.layout
#import megrok.resourcelibrary

from hurry.jquery import jquery
from zope.interface import Interface
from megrok.z3cform.base import IFormLayer
from hurry.resource import Library, ResourceInclusion, rollup

#Not sure if this is needed after using megrok.z3cform.ui
from z3c.formui.interfaces import IDivFormLayer

class IUVCSiteLayer(IFormLayer, IDivFormLayer):
    pass


class IUVCSiteSkin(IUVCSiteLayer, grok.IDefaultBrowserLayer):
    grok.skin('uvcsiteskin')


class StylesDirectory(grok.DirectoryResource):
    grok.name('styles')
    grok.path('styles')


styles = Library('styles')
nva = ResourceInclusion(styles, 'nva.css')
css = ResourceInclusion(styles, 'main.css', depends=[nva])


class ScriptsDirectory(grok.DirectoryResource):
    grok.name('javascripts')
    grok.path('javascripts')


scripts = Library('javascripts')
tablesorter = ResourceInclusion(scripts, 'jquery.tablesorter.js', [jquery])
Table = ResourceInclusion(scripts, 'mytable.js', [tablesorter]) 

tooltip = ResourceInclusion(scripts, 'tools.tooltip-1.1.0.js', [jquery])
Forms = ResourceInclusion(scripts, 'mytooltip.js', [tooltip])

class StandardLayout(megrok.layout.Layout):
    grok.context(Interface)

    def update(self):
        css.need()
        rollup()
