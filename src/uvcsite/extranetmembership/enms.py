# -*- coding: utf-8 -*-

import grok
import megrok.pagelet

from uvcsite import uvcsiteMF as _
from zope.component import getUtility
from uvcsite.interfaces import IUVCSite
from zope.formlib.form import setUpWidgets
from megrok.pagelet.component import FormPageletMixin
from uvcsite.extranetmembership.interfaces import (IUserManagement,
                 IExtranetMember)
from uvcsite.extranetmembership.custom_fields import *
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.securitypolicy.interfaces import IPrincipalRoleManager


class ENMSIndex(megrok.pagelet.Pagelet):
    grok.context(IUVCSite)

    def getUserGroup(self):
        principal = "0101010001" #self.request.principal.hauptuser
        um = getUtility(IUserManagement)
        return um.getUserGroup(principal)


class ENMSCreateUser(FormPageletMixin, grok.Form):
    grok.context(IUVCSite)
    form_fields = grok.Fields(IExtranetMember)
    form_fields['mnr'].custom_widget = LoginNameWidgetHidden 
    form_fields['roles'].custom_widget = MultiCheckBoxVocabularyWidget

    def setUpWidgets(self, ignore_request=False):
        #BBB Die Werte mussen hier erst noch errechnet werden.
        principal = "0101010001" #self.request.principal.hauptuser
        um = getUtility(IUserManagement)
        ll = len(um.getUserGroup(principal))
        value = principal + '-' + str(ll)
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
        hauptuser = kw.get('mnr').split('-')[0]
        utility = getUtility(IHomeFolderManager)
        #principal_roles = IPrincipalRoleManager(utility.homeFolderBase[hauptuser])
        #principal_roles.assignRoleToPrincipal( utility.homeFolderRole, kw.get('mnr') )
	self.flash('Der Mitbenutzer wurde gespeichert')
        self.redirect(self.url(self.context))


class ENMSUpdateUser(FormPageletMixin, grok.Form):
    """ A Form for updating a User in ENMS"""
    grok.context(IUVCSite)
    form_fields = grok.Fields(IExtranetMember)
    form_fields['mnr'].custom_widget = LoginNameWidgetHidden 
    form_fields['roles'].custom_widget = MultiCheckBoxVocabularyWidget

    def setUpWidgets(self, ignore_request=False):
        #BBB Die Werte mussen hier erst noch errechnet werden.
        principal = "0101010001" #self.request.principal.hauptuser
        #import pdb; pdb.set_trace()
        id = self.request.get('cn')
        um = getUtility(IUserManagement)
        user = {}
        if id:
            user = um.getUser(id)
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
        um.updateUser(**kw)
        self.redirect(self.url(self.context))

    @grok.action(_(u"Entfernen"))
    def entfernen(self, **kw):
        um = getUtility(IUserManagement)
        key = kw.get('mnr')
        um.delUser(key)
        self.redirect(self.url(self.context))

