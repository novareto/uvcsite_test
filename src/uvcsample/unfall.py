# -*- coding: utf-8 -*- 
# Copyright (c) 2007-2008 NovaReto GmbH 
# cklinger@novareto.de 

import grok
import zope.schema
import megrok.z3cform
import uvcsite.interfaces


from uvcsite import Content
from uvcsite.interfaces import ISidebar
from uvcsite.viewlets.utils import MenuItem 
from zope.interface import Interface
from zope.app.homefolder.interfaces import IHomeFolder

from z3c.form import field, form, button
from hurry.workflow.interfaces import IWorkflowInfo
from zope.app.container.interfaces import INameChooser
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from uvcsample.interfaces import IUnfall
from z3c.form.browser import radio


class Unfall(Content):
    grok.implements(IUnfall)
    name = None


class UnfallContainer(grok.Container):
    pass


@grok.subscribe(uvcsite.interfaces.IHomeFolder, grok.IObjectAddedEvent)
def addContainer(object, event):
    object['unfall'] = UnfallContainer()


class Index(megrok.z3cform.PageDisplayForm):
    grok.context(IUnfall)
    fields = field.Fields(IUnfall)
    grok.require('uvc.ViewContent')


class Edit(megrok.z3cform.PageEditForm):
    grok.context(IUnfall)
    form.extends(form.EditForm)
    fields = field.Fields(IUnfall)
    grok.require('uvc.EditContent')

    @button.buttonAndHandler(u'Versenden', name='applyView')
    def handleApplyView(self, action):
        IWorkflowInfo(self.context).fireTransition('publish')
	self.flash(u"Unfall wurde versendet")
        self.redirect(self.url(self.context))


class Add(megrok.z3cform.PageAddForm):
    grok.context(UnfallContainer)
    fields = field.Fields(IUnfall)
    fields['unfustdor'].widgetFactory = radio.RadioFieldWidget
    grok.require('uvc.AddContent')

    label=u"Elektronische Unfallanzeige"

    def create(self, data):
	unfall = Unfall()
        form.applyChanges(self, unfall, data) 
	return unfall

    def add(self, object):
	name = INameChooser(self.context).chooseName('', object)
	self.context[name] = object
        return object

    def nextURL(self):
	self.flash(u"Unfall wurde angelegt")
	hF = IHomeFolder(self.request.principal).homeFolder
        return self.url(hF)


class AddMenuItem(MenuItem):
    grok.name('Unfall')
    grok.context(Interface)
    grok.viewletmanager(ISidebar)

    urlEndings = "add"
    @property
    def url(self):
	hF = IHomeFolder(self.request.principal).homeFolder
	return self.view.url(hF, 'unfall/add')
    
