import grok
from persistent import Persistent
from zope.component import getUtility
from zope.interface import implements
from zope.location.interfaces import ILocation
from interfaces import IUVCAuth, IMasterUser
from zope.app.authentication.principalfolder import PrincipalInfo, Principal
from zope.app.authentication.interfaces import IPrincipal
from uvcsite.extranetmembership.interfaces import IUserManagement
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.authentication.httpplugins import HTTPBasicAuthCredentialsPlugin
import zope.interface
from zope.publisher.interfaces import IRequest
from zope.event import notify


@grok.adapter(IPrincipal)
@grok.implementer(IMasterUser)
def masteruser(self):
    if not "-" in self.id:
        return self
    master_id = self.id.split('-')[0]    
    return Principal(master_id) 


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

    def authenticateCredentials(self, credentials):
        if not (credentials and 'login' in credentials and 'password' in credentials):
            return
        login, password = credentials['login'], credentials['password']
        utility = getUtility(IUserManagement)
	user = utility.getUser(login)
	if not user:
	    return
        if password != user.get('passwort'):
	    return
	return PrincipalInfo(login, login, login, login)

    def principalInfo(self, id):
        return None
