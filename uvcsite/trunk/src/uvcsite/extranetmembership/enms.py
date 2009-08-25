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
from uvcsite.extranetmembership.custom_fields import *
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from uvcsite.interfaces import IMyHomeFolder


class ENMS(megrok.layout.Page):
    grok.context(IMyHomeFolder)
    grok.require('uvc.ManageCoUsers')

    def getUserGroup(self):
        principal = "0101010001" #self.request.principal.hauptuser
        um = getUtility(IUserManagement)
        return um.getUserGroups(principal)


class ENMSCreateUser(Form, grok.Form):
    grok.context(IMyHomeFolder)
    grok.require('uvc.ManageCoUsers')
    form_fields = grok.Fields(IExtranetMember)
    form_fields['mnr'].custom_widget = LoginNameWidgetHidden
    form_fields['rollen'].custom_widget = MultiCheckBoxVocabularyWidget

    def setUpWidgets(self, ignore_request=False):
        #BBB Die Werte mussen hier erst noch errechnet werden.
        principal = "0101010001" #self.request.principal.hauptuser
        um = getUtility(IUserManagement)
        ll = len(um.getUserGroups(principal))
        value = principal + '-' + str(ll+1)
        data={'mnr': value}
        self.adapters = {}
        self.widgets = setUpWidgets(
                         self.form_fields,
                         self.prefix,
                         self.context,
                         self.request,
                         ignore_request=ignore_request,
                         data=data)

    @grok.action(_(u"Anlegen"))
    def anlegen(self, **kw):
        um = getUtility(IUserManagement)
        um.addUser(**kw)
        # Setting Home Folder Rights
        for role in kw.get('rollen'):
            principal_roles = IPrincipalRoleManager(self.context[role])
            principal_roles.assignRoleToPrincipal('uvc.Editor', kw.get('mnr'))
        self.flash('Der Mitbenutzer wurde gespeichert')
        self.redirect(self.url(self.context))


class ENMSUpdateUser(Form, grok.Form):
    """ A Form for updating a User in ENMS"""
    grok.context(IMyHomeFolder)
    form_fields = grok.Fields(IExtranetMember)
    form_fields['mnr'].custom_widget = LoginNameWidgetHidden
    form_fields['rollen'].custom_widget = MultiCheckBoxVocabularyWidget
    grok.require('uvc.ManageCoUsers')

    def setUpWidgets(self, ignore_request=False):
        #BBB Die Werte mussen hier erst noch errechnet werden.
        principal = "0101010001" #self.request.principal.hauptuser
        #import pdb; pdb.set_trace()
        id = self.request.get('cn')
        um = getUtility(IUserManagement)
        user = {}
        if id:
            user = um.getUser(id)
            user['mnr'] = id
        data=user
        self.adapters = {}
        self.widgets = setUpWidgets(
                         self.form_fields,
                         self.prefix,
                         self.context,
                         self.request,
                         ignore_request=ignore_request,
                         data=data)

    @grok.action(_(u"Bearbeiten"))
    def anlegen(self, **kw):
        um = getUtility(IUserManagement)
        um.updUser(**kw)
        for role in self.context.values():
            principal_roles = IPrincipalRoleManager(role)
            principal_roles.removeRoleFromPrincipal('uvc.Editor',
                                                    kw.get('mnr'))
        for role in kw.get('rollen'):
            principal_roles = IPrincipalRoleManager(self.context[role])
            principal_roles.assignRoleToPrincipal('uvc.Editor', kw.get('mnr'))
        self.flash('Der Mitbenutzer wurde gespeichert')
        self.redirect(self.url(self.context))

    @grok.action(_(u"Entfernen"))
    def entfernen(self, **kw):
        um = getUtility(IUserManagement)
        key = kw.get('mnr')
        um.delUser(key)
        for role in self.context.values():
            principal_roles = IPrincipalRoleManager(role)
            principal_roles.removeRoleFromPrincipal('uvc.Editor',
                            kw.get('mnr'))
        self.redirect(self.url(self.context))
