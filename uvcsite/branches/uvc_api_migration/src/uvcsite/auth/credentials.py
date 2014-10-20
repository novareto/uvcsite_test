# -*- coding: utf-8 -*-

import uvclight
from uvcsite.extranetmembership.interfaces import IUserManagement
from uvclight.auth import ICredentials
from zope.component import getUtility


class SimpleCredentials(uvclight.GlobalUtility):
    uvclight.name('simple')
    uvclight.implements(ICredentials)

    def account(self, login):
        manager = getUtility(IUserManagement)
        return manager.getUser(login)

    def assert_credentials(self, account, password):
        return account['passwort'] == password

    def log_in(self, username, password):
        account = self.account(username)
        if account is None:
            return None
        if self.assert_credentials(account, password):
            return account
        return False
