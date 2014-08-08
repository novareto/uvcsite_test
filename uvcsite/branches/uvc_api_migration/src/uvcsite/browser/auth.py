# -*- coding: utf-8 -*-

import uvclight
from ..interfaces import ILoginForm, ICredentials
from cromlech.browser import exceptions
from cromlech.browser import getSession
from dolmen.forms.base import FAILURE, SuccessMarker
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.interface import Interface
from zope.event import notify


class Login(uvclight.Form):
    uvclight.name('login')
    uvclight.context(Interface)
    uvclight.require('zope.Public')

    fields = uvclight.Fields(ILoginForm)

    @uvclight.action(u'Login')
    def log_me(self):
        data, errors = self.extractData()
        if errors:
            self.submissionError = errors
            return FAILURE

        # credentials here
        site = getSite()
        if site is None:
            self.flash(u"You can't login here.")
            return SuccessMarker(
                'Login failed', False, url=self.url(self.context), code=302)

        credentials = getattr(site, 'credentials', None)
        if not credentials:
            self.flash(u"Missing credentials.")
            return SuccessMarker(
                'Login failed', False, url=self.url(self.context), code=302)

        for credential in credentials:
            credentials_manager = getUtility(ICredentials, name=credential)
            account = credentials_manager.log_in(**data)
            if account:
                session = getSession()
                session['username'] = data['username']
                self.flash(u"Login successful.")
                principal = uvclight.auth.Principal(data['username'])
                notify(uvclight.UserLoggedInEvent(principal))
                return SuccessMarker(
                    'Login successful', True, url=self.url(self.context),
                    code=302)

        self.flash(u'Login failed.')
        return FAILURE


class UnauthorizedPage(uvclight.Page):
    uvclight.name('')
    uvclight.context(exceptions.HTTPUnauthorized)
    uvclight.require('zope.Public')

    def render(self):
        obj = self.context.__parent__
        self.flash(
            u"This page is protected and you're not allowed."
            u" Please login.")
        self.redirect(self.url(obj) + '/login')

    
class ForbiddenPage(uvclight.Page):
    uvclight.name('')
    uvclight.context(exceptions.HTTPForbidden)
    uvclight.require('zope.Public')

    def render(self):
        return u"This page is protected and you don't have the credentials."
