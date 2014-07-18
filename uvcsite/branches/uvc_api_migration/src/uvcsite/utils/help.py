# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import uvclight
import uvcsite

from cromlech.browser import ITemplate, ISlot
from grokcore.component import adapter, implementer
from uvc.design.canvas import IAboveContent
from zope.component import getMultiAdapter
from zope.interface import Interface


class HelpManager(uvclight.ViewletManager):
    """ ViewletManager für HilfeSeiten
    """
    uvclight.context(Interface)
    uvclight.name('uvc.hilfen')

    def getHelpPages(self):
        rc = []
        for viewlet in self.viewlets:
            if IHelpPage.providedBy(viewlet):
                rc.append(viewlet)
        return rc 

    def getViewlets(self):
        rc = []
        for viewlet in self.viewlets:
            if not IHelpPage.providedBy(viewlet):
                rc.append(viewlet)
        return rc 

    def render(self):
        template = getMultiAdapter((self, self.request), ITemplate)
        return template.render(
            self, **self.namespace())


@adapter(HelpManager, Interface)
@implementer(ITemplate)
def HelpManagerTemplate(context, request):
    return uvclight.get_template('helpmanagertemplate.pt', __file__)


class Help(uvclight.Viewlet):
    uvclight.viewletmanager(IAboveContent)
    uvclight.context(Interface)
    uvclight.order(9999)

    def render(self):
        helpmanager = getMultiAdapter(
            (self.context, self.request, self.view), ISlot, name=u'uvc.hilfen')
        helpmanager.update()
        return helpmanager.render()



class IHelpPage(Interface):
    """Marker interface
    """


class HelpPage(uvclight.Viewlet):
    uvclight.viewletmanager(HelpManager)
    uvclight.implements(IHelpPage)
    uvclight.baseclass()

    def update(self):
        self.response = self.request.response

    def namespace(self):
        return {'settings_overrides': {'input_encoding': 'utf-8',
                                       'output_encoding': 'unicode',
                                       'stylesheet': '',
                                       'stylesheet_path': None,
                                       'embed_stylesheet' :0,
                }}

