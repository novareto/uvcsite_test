from persistent import Persistent
from zope.component import getUtility
from zope.interface import implements
from zope.location.interfaces import ILocation
from interfaces import IUVCAuth
from zope.app.authentication.principalfolder import PrincipalInfo
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.authentication.httpplugins import HTTPBasicAuthCredentialsPlugin


def setup_pau(pau):
    pau['principals'] = UVCAuthenticator('contact.principals.')
    pau.authenticatorPlugins = ('principals', 'groups')
    pau['basic'] = basic = HTTPBasicAuthCredentialsPlugin()
    pau.credentialsPlugins = ('No Challenge if Authenticated', 'basic',)

class UVCAuthenticator(Persistent):
    implements(IUVCAuth, IAuthenticatorPlugin, ILocation)
    __parent__ = __name__ = None
    
    def __init__(self, prefix=u''):
        self.prefix = prefix


    def getRolesForPrincipal(self, id):
	roles=[]
        utility = getUtility(IUserManagement)
	user = utility.getUser(id)
	if user:
	    roles = user.get('rollen', [])
	return roles 

    def authenticateCredentials(self, credentials):
        if not (credentials and 'login' in credentials and 'password' in credentials):
            return
        login, password = credentials['login'], credentials['password']
        utility = getUtility(IUserManagement)
	user = utility.getUser(login)
	if user:
	    if password == user.get('passwort'):
	        id = user.get('mnr').split('-')[0]
		title = "%s-%s" %(user.get('mnr'),user.get('az'))
		#PrincipalInfo('users.foo', 'foo', 'Foo', 'An over-used term.')
	        pi = PrincipalInfo(login, id, id, title)
	        return pi

    def principalInfo(self, id):
        """Principal Info"""
        if id.startswith(self.prefix):
            login = id[len(self.prefix):]
            if login == "hans":
                return Principal(self.prefix+login, login, login, login)	
