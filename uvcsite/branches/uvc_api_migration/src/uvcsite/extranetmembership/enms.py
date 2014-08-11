# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

import uvclight
import uvcsite

from dolmen.forms import base
from dolmen.forms.base import Fields
from dolmen.menu import menuentry
from uvc.homefolder import IHomefolder
from uvc.design.canvas import IPersonalPreferences, IPersonalMenu
from uvcsite import uvcsiteMF as _
from zope.component import getUtility
from zope.securitypolicy.interfaces import IPrincipalRoleManager

from .interfaces import IUserManagement, IExtranetMember
from .vocabulary import vocab_berechtigungen
from grokcore.chameleon.components import ChameleonPageTemplateFile


class ENMS(uvclight.Page):
    uvclight.title('Mitbenutzerverwaltung')
    uvclight.context(IHomefolder)
    uvclight.require('uvc.ManageCoUsers')

    template = uvclight.get_template('enms.cpt', __file__)

    def getUserGroup(self):
        principal = self.request.principal.id
        um = getUtility(IUserManagement)
        return um.getUserGroups(principal)

    def displayRoles(self, roles):
        rc = []
        vb = vocab_berechtigungen(None)
        for role in roles:
            try:
                rc.append(vb.getTerm(role).title)
            except:
                print role
                pass
        return rc


class ENMSCreateUser(uvclight.Form):
    """ Simple Form which displays values from a Dict"""
    uvclight.context(IHomefolder)
    uvclight.require('uvc.ManageCoUsers')

    label = u"Mitbenutzer anlegen"
    description = u"Nutzen Sie diese Form um einen neuen Mitbenutzer anzulegen"

    ignoreContent = False

    fields = Fields(IExtranetMember)

    def updateForm(self):
        super(ENMSCreateUser, self).updateForm()
        self.fieldWidgets.get('form.field.mnr').template = uvclight.get_template('mnr.cpt', __file__)

    def getNextNumber(self, groups):
        all_azs = []
        for group in groups:
            all_azs.append(group['az'])
        if not all_azs:
            return 1
        return int(max(all_azs)) + 1

    def getDefaultData(self):
        principal = self.request.principal.id
        um = getUtility(IUserManagement)
        all_users = self.getNextNumber(um.getUserGroups(principal))
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
        homeFolder = IHomefolder(principal)
        self.redirect(self.url(homeFolder, 'enms'))


class ENMSUpdateUser(uvclight.Form):
    """ A Form for updating a User in ENMS"""
    uvclight.context(IHomefolder)
    uvclight.require('uvc.ManageCoUsers')

    label = u"Mitbenutzer verwalten"
    description = u"Nutzen Sie diese Form um die Daten eines Mitbenutzers zu pflegen."

    fields = Fields(IExtranetMember)
    ignoreContent = False

    templates = {
        "mnr": uvclight.get_template('mnr.cpt', __file__),
        "pw": uvclight.get_template('password.cpt', __file__),
        "confirm": uvclight.get_template('password.cpt', __file__),
        }
    
    def getDefaultData(self):
        principal = self.request.principal.title
        id = "%s-%s" % (self.request.principal.id, self.request.form.get('cn'))
        user = {}
        if self.request.form.get('cn'):
            um = getUtility(IUserManagement)
            user = um.getUser(id)
            user['mnr'] = id
            user['confirm'] = user['passwort']
        return user

    def update(self):
        data = self.getDefaultData()
        self.setContentData(base.DictDataManager(data))

    def updaiteForm(self):
        super(ENMSUpdateUser, self).updateForm()
        mnr = self.fieldWidgets.get('form.field.mnr')
        pw = self.fieldWidgets.get('form.field.passwort')
        confirm = self.fieldWidgets.get('form.field.confirm')

        mnr.template = self.templates.get('mnr')
        pw.template = self.templates.get('pw')
        confirm.template = self.templates.get('confirm')

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
        homeFolder = IHomefolder(principal)
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


class ChangePasswordMenu(uvclight.MenuItem):
    uvclight.title(u'Passwort ändern')
    uvclight.require('zope.View')
    uvclight.menu(IPersonalMenu)

    @property
    def action(self):
       return self.view.url(
           IHomeFolder(self.request.principal).homeFolder, 'changepassword')


class ChangePassword(uvclight.Form):
    """ A Form for updating a User in ENMS"""
    uvclight.title(u'Passwort ändern')
    uvclight.context(IHomefolder)
    label = _(u'Passwort ändern')
    description = _(u'Hier können Sie Ihr Passwort ändern')
    #uvcsite.menu(uvcsite.PersonalMenu)
    uvclight.require('zope.View')

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
