# -*- coding: utf-8 -*-

import grok
import megrok.layout

from uvcsite import uvcsiteMF as _
from zope.component import getUtility
from uvcsite.interfaces import IUVCSite
from zope.formlib.form import setUpWidgets
from megrok.layout.components import Form
from uvcsite.extranetmembership.interfaces import (IUserManagement,
                 IExtranetMember)
from zope.app.homefolder.interfaces import IHomeFolder
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from uvcsite.interfaces import IMyHomeFolder, IPersonalPreferences, IPersonalMenu
from dolmen.menu import menuentry
from megrok.z3cform.base import PageForm, Fields, button
from z3c.form.browser.checkbox import CheckBoxFieldWidget


class ENMS(megrok.layout.Page):
    grok.title('Mitbenutzerverwaltung')
    grok.context(IMyHomeFolder)
    grok.require('uvc.ManageCoUsers')

    def getUserGroup(self):
        principal = self.request.principal.id
        um = getUtility(IUserManagement)
        return um.getUserGroups(principal)


class ENMSCreateUser(PageForm):
    grok.context(IMyHomeFolder)
    grok.require('uvc.ManageCoUsers')
    #template = grok.PageTemplateFile('templates/form.pt')
    label = u"Mitbenutzer anlegen"
    description = u"Nutzen Sie diese Form um einen neuen Mitbenutzer anzulegen"

    fields = Fields(IExtranetMember)
    fields['rollen'].widgetFactory = CheckBoxFieldWidget

    def getContent(self):
        principal = self.request.principal.id
        um = getUtility(IUserManagement)
        ll = len(um.getUserGroups(principal))
        value = principal + '-' + str(ll+1)
        rollen = self.context.keys()
        return {'mnr': value, 'rollen': rollen}

    def updateWidgets(self):
        super(ENMSCreateUser, self).updateWidgets()
        mnr = self.widgets['mnr']

    @button.buttonAndHandler(_(u"Anlegen"))
    def anlegen(self, action):
        data, errors = self.extractData()
        if errors:
            self.flash(self.formErrorsMessage, type='error')
            return
        um = getUtility(IUserManagement)
        um.addUser(**data)
        # Setting Home Folder Rights
        for role in data.get('rollen'):
            principal_roles = IPrincipalRoleManager(self.context[role])
            principal_roles.assignRoleToPrincipal('uvc.Editor', data.get('mnr'))
        self.flash(_(u'Der Mitbenutzer wurde gespeichert'))
        principal = self.request.principal
        homeFolder = IHomeFolder(principal).homeFolder
        self.redirect(self.url(homeFolder, 'enms'))


class ENMSUpdateUser(PageForm):
    """ A Form for updating a User in ENMS"""
    grok.context(IMyHomeFolder)
    fields = Fields(IExtranetMember)
    fields['rollen'].widgetFactory = CheckBoxFieldWidget
    grok.require('uvc.ManageCoUsers')

    def updateWidgets(self):
        super(ENMSUpdateUser, self).updateWidgets()
        mnr = self.widgets['mnr']
        #mnr.disabled = 'disabled'

    def getContent(self):
        principal = self.request.principal.id
        id = self.request.get('cn')
        user = {} 
        if id: 
            um = getUtility(IUserManagement)
            user = um.getUser(id)
            user['mnr'] = id
            user['confirm'] = user['passwort']
        return user 

    @button.buttonAndHandler(_(u"Bearbeiten"))
    def anlegen(self, action):
        data, errors = self.extractData()
        if errors:
            self.flash(self.formErrorsMessage, type='error')
            return
        um = getUtility(IUserManagement)
        um.updUser(**data)
        for role in self.context.values():
            principal_roles = IPrincipalRoleManager(role)
            principal_roles.removeRoleFromPrincipal('uvc.Editor',
                                                    data.get('mnr'))
        for role in data.get('rollen'):
            principal_roles = IPrincipalRoleManager(self.context[role])
            principal_roles.assignRoleToPrincipal('uvc.Editor', data.get('mnr'))
        self.flash(_(u'Der Mitbenutzer wurde gespeichert'))
        principal = self.request.principal
        homeFolder = IHomeFolder(principal).homeFolder
        self.redirect(self.url(homeFolder, 'enms'))

    @button.buttonAndHandler(_(u"Entfernen"))
    def entfernen(self, action):
        data, errors = self.extractData()
        um = getUtility(IUserManagement)
        key = data.get('mnr')
        um.deleteUser(key)
        for role in self.context.values():
            principal_roles = IPrincipalRoleManager(role)
            principal_roles.removeRoleFromPrincipal('uvc.Editor',
                            data.get('mnr'))
        self.flash(_(u'Der Mitbenutzer wurde entfernt.'))
        principal = self.request.principal
        homeFolder = IHomeFolder(principal).homeFolder
        self.redirect(self.url(homeFolder, 'enms'))


@menuentry(IPersonalMenu)
class ChangePassword(PageForm):
    """ A Form for updating a User in ENMS"""
    grok.title(u'Passwort ändern')
    grok.context(IUVCSite)
    title = _(u'Passwort ändern')
    label = _(u'Hier können Sie Ihr Passwort ändern')

    fields = Fields(IExtranetMember).select('passwort', 'confirm')
    ignoreContext = True

    @button.buttonAndHandler(_(u"Bearbeiten"))
    def changePasswort(self, action):
        data, errors = self.extractData()
        if errors:
            self.flash(self.formErrorsMessage, type='error')
            return
        um = getUtility(IUserManagement)
        principal = self.request.principal.id
        data['mnr'] = principal
        um.updatePasswort(**data)
        self.flash(_(u'Ihr Passwort wurde gespeichert!'))
        self.redirect(self.url(self.context))
