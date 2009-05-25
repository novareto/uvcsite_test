from zope.interface import implements
from zope.component import getUtility
from zope.app.security.interfaces import IAuthentication
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from zope.app.security.settings import Allow, Deny, Unset

_marker = object() 

class CustomPrincipalRoleMap(object):
    """Mappings between principals and roles."""

    implements(IPrincipalRoleMap)

    _prefix=_marker

    def __init__(self,context):
        self.context=context
        pau = getUtility(IAuthentication)
        try:
            self.userfolder = pau.get('principals')
            self._prefix=unicode(self.userfolder.prefix)
        except:
            pass

    def getPrincipalsForRole(self,role_id):
        raise NotImplementedError

    def getSetting(self,role_id, principal_id):
        raise NotImplementedError

    def getPrincipalsAndRoles(self):
        raise NotImplementedError

    def getRolesForPrincipal(self,principal_id):
        """Get the roles granted to a principal.

        Return the list of (role id, setting) assigned or removed from
        this principal.

        If no roles have been assigned to
        this principal, then the empty list is returned."""
	if principal_id.startswith('zope'):
	    return []
	roleslist = []
	if len(principal_id) == 10:
	    roleslist.append(('uvc.ManageMitbenutzer', Allow))
	for roles in self.userfolder.getRolesForPrincipal(principal_id):
	    if roles.startswith('uvc.'):
                roleslist.append((roles, Allow))
	## Default Rolle 	
	roleslist.append(('uvc.RolleMember', Allow))
	return roleslist 
