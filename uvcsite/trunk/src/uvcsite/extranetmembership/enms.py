# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite
import megrok.layout

from megrok import navigation
from zeam.form import base
from dolmen.menu import menuentry
from uvcsite import uvcsiteMF as _
from dolmen.forms.base import Fields 
from zope.component import getUtility
from uvcsite.interfaces import IUVCSite
from zope.app.homefolder.interfaces import IHomeFolder
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from uvcsite.interfaces import IMyHomeFolder, IPersonalPreferences, IPersonalMenu
from uvcsite.extranetmembership.interfaces import IUserManagement, IExtranetMember


class ENMS(megrok.layout.Page):
    grok.title('Mitbenutzerverwaltung')
    grok.context(IMyHomeFolder)
    grok.require('uvc.ManageCoUsers')

    def getUserGroup(self):
        principal = self.request.principal.id
        um = getUtility(IUserManagement)
        return um.getUserGroups(principal)

    def displayRoles(self, roles):
        return ', '.join(roles)


class ENMSCreateUser(uvcsite.Form):
    """ Simple Form which displays values from a Dict"""
    grok.context(IMyHomeFolder)
    grok.require('uvc.ManageCoUsers')

    label = u"Mitbenutzer anlegen"
    description = u"Nutzen Sie diese Form um einen neuen Mitbenutzer anzulegen"

    ignoreContent = False

    fields = Fields(IExtranetMember)

    def updateForm(self):
        super(ENMSCreateUser, self).updateForm()
        self.fieldWidgets.get('form.field.mnr').template = grok.PageTemplateFile('templates/mnr.pt')


    def getDefaultData(self):
        principal = self.request.principal.id
        um = getUtility(IUserManagement)
        all_users = len(um.getUserGroups(principal)) + 1
        user = principal + '-' + str(all_users).zfill(2)
        rollen = self.context.keys()
        return {'mnr': user, 'rollen': rollen}

    def update(self):
        data = self.getDefaultData() 
        self.setContentData(base.DictDataManager(data))

    @base.action(_(u"Anlegen"))
    def anlegen(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
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


class ENMSUpdateUser(uvcsite.Form):
    """ A Form for updating a User in ENMS"""
    grok.context(IMyHomeFolder)
    grok.require('uvc.ManageCoUsers')

    label = u"Mitbenutzer verwalten"
    description = u"Nutzen Sie diese Form um die Daten eines Mitbenutzers zu pflegen."

    fields = Fields(IExtranetMember)
    ignoreContent = False

    def getDefaultData(self):
        principal = self.request.principal.title
        id = "%s-%s" % (self.request.principal.title, self.request.get('cn'))
        user = {} 
        if self.request.get('cn'): 
            um = getUtility(IUserManagement)
            user = um.getUser(id)
            user['mnr'] = id 
            user['confirm'] = user['passwort']
        return user 

    def update(self):
        data = self.getDefaultData() 
        self.setContentData(base.DictDataManager(data))

    def updateForm(self):
        super(ENMSUpdateUser, self).updateForm()
        mnr = self.fieldWidgets.get('form.field.mnr')
        pw = self.fieldWidgets.get('form.field.passwort')
        confirm = self.fieldWidgets.get('form.field.confirm')

        mnr.template = grok.PageTemplateFile('templates/mnr.pt')
        pw.template = grok.PageTemplateFile('templates/password.pt')
        confirm.template = grok.PageTemplateFile('templates/password.pt')

    @base.action(_(u"Bearbeiten"))
    def anlegen(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
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

    @base.action(_(u"Entfernen"))
    def entfernen(self):
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


class ChangePassword(uvcsite.Form):
    """ A Form for updating a User in ENMS"""
    grok.title(u'Passwort ändern')
    grok.context(IMyHomeFolder)
    label = _(u'Passwort ändern')
    description = _(u'Hier können Sie Ihr Passwort ändern')
    navigation.sitemenuitem(uvcsite.IPersonalMenu)

    fields = Fields(IExtranetMember).select('passwort', 'confirm')
    ignoreContext = True

    @base.action(_(u"Bearbeiten"))
    def changePasswort(self):
        data, errors = self.extractData()
        if errors:
            self.flash('Es sind Fehler aufgetreten', type='error')
            return
        um = getUtility(IUserManagement)
        principal = self.request.principal.id
        data['mnr'] = principal
        um.updatePasswort(**data)
        self.flash(_(u'Ihr Passwort wurde gespeichert!'))
        self.redirect(self.url(self.context))
