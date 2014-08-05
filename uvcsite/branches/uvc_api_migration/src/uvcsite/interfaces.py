# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.schema import TextLine, Password


class ICredentials(Interface):

    def assert_credentials(username, password):
        """Returns a boolean
        """


class IFolderListingTable(Interface):
    pass


class IFolderColumnTable(Interface):
    pass


class IRoles(Interface):
    pass


class ILoginForm(Interface):

    username = TextLine(
        title=u'Username',
        required=True)

    password = Password(
        title=u"Password",
        required=True)
