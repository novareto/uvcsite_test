import grok
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.app.authentication.interfaces import IAuthenticatedPrincipalCreated

users = [
          {'mnr':'0101010001', 'passwort':'passwort', 'email':'test@test.de'},
          {'mnr':'0101010002', 'passwort':'passwort', 'email':'test@test.de'},
        ]


class UserManagement(grok.GlobalUtility):
    """ Utility for Usermanagement """
    grok.implements(IUserManagement)

    def updUser(self, **kwargs):
        """Updates a User"""

    def deleteUser(self, mnr):
        """Delete the User"""

    def addUser(self, **kwargs):
        """Adds a User"""

    def getUser(self, mnr):
        """Return a User"""
        for user in users:
            if user.get('mnr') == mnr:
                return user
        return None

    def getUserGroups(self, mnr):
        """Return a group of Users"""
        return users

    def updatePasswort(self, **kwargs):
        """Change a passwort from a user"""
