# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
import megrok.z3ctable

from uvcsite import uvcsiteMF as _
from zope.interface import Interface
from uvcsite.viewlets.utils import MenuItem
from uvcsite.interfaces import IUVCSite, IGlobalMenu
from uvcsite.helpsystem.interfaces import IHelpFolder
from zope.app.authentication.interfaces import IPrincipal
from uvcsite.content import ProductFolder, IProductFolder, contenttype
from page import HelpPage


class HelpFolder(ProductFolder):
    grok.implements(IProductFolder, IHelpFolder)
    grok.title('Hilfe')
    grok.name(u'In diesem Ordner finden Sie Hilfe Dokumente')
    grok.description(u'Sie knnen auf die einzelnen Dokumente
                       klicken um die Hilfe anzueigen!')

    contenttype(HelpPage)


class Hilfe(MenuItem):
    grok.name(_(u'Hilfe'))
    grok.context(Interface)
    grok.viewletmanager(IGlobalMenu)
    grok.require('zope.ManageSite')

    title= _(u'Hilfe')
    urlEndings = "hilfe"
    viewURL = "hilfe"


@grok.subscribe(IUVCSite, grok.IObjectAddedEvent)
def addHelpFolder(context, event):
    context['hilfe'] = HelpFolder()
