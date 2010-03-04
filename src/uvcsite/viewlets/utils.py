# -*- coding: utf-8 -*-

import grok

from z3c.menu.simple.menu import GlobalMenuItem
from z3c.menu.simple.menu import ContextMenuItem
from zope.traversing.browser import absoluteURL
from zope.app.homefolder.interfaces import IHomeFolder
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.app.security.interfaces import IUnauthenticatedPrincipal


class MenuItem(grok.Viewlet, GlobalMenuItem):
    grok.baseclass()
    template = ViewPageTemplateFile('templates/menu_item.pt')

    def home_folder_url(self, url=False):
        principal = self.request.principal
        if IUnauthenticatedPrincipal.providedBy(principal):
            return
        homeFolder = IHomeFolder(principal).homeFolder
        if url:
            homeFolder = absoluteURL(homeFolder, self.request)
        return homeFolder

    def render(self):
        # This method is for grok not to say template or render needed!
        return self.template()



class DocumentAction(grok.Viewlet, ContextMenuItem):
    grok.baseclass()

    image = "pdf.png"
    template = ViewPageTemplateFile('templates/document_action.pt')

    
    def image_url(self):
        url = "%s/@@/uvc.skin/%s" % (self.view.application_url(), self.image)
        return url

    def render(self):
        # This method is for grok not to say template or render needed!
        return self.template()
