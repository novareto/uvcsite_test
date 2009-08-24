import grok
from uvcsite.extranetmembership.interfaces import IUserManagement

users = [
          {'cn':'0101010001', 'passwort':'passwort', 'email':'test@test.de'},
          {'cn':'0101010002', 'passwort':'passwort', 'email':'test@test.de'},
        ]

class UserManagement(grok.GlobalUtility):
    """ Utility for Usermanagement """
    grok.implements(IUserManagement)

    def updateUser(self, **kwargs):
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
