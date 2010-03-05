# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok

from uvcsite import uvcsiteMF as _
from zope.interface import Interface
from uvcsite.viewlets.utils import MenuItem
from uvcsite.interfaces import IUVCSite, IGlobalMenu
from uvcsite.helpsystem.interfaces import IHelpFolder
from uvcsite.content import ProductFolder, IProductFolder, contenttype
from page import HelpPage
from dolmen.menu import menuentry
from uvc.layout.menus import GlobalMenu

@menuentry(IGlobalMenu)
class HelpFolder(ProductFolder):
    grok.implements(IProductFolder, IHelpFolder)
    grok.title('Hilfe')
    grok.name('Hifle')
    grok.description(_(u'Sie koennen auf die einzelnen Dokumente'
                      ' klicken um die Hilfe anzueigen!'))

    contenttype(HelpPage)

    # No autopopulation on Startup!!!
    inHomeFolder = False


@grok.subscribe(IUVCSite, grok.IObjectAddedEvent)
def addHelpFolder(context, event):
    context['hilfe'] = HelpFolder()
