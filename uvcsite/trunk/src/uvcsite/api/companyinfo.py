import grok
from zope.interface import Interface
from uvcsite.api.interfaces import ICompanyInfo
from zope.app.authentication.interfaces import IPrincipal

class CompanyInfo(grok.Adapter):
    grok.implements(ICompanyInfo)
    #grok.adapts(IPrincipal)
    grok.context(IPrincipal)

    def __init__(self, principal):
	self.principal = principal

    def getHauptUser(self):
	return str(self.principal.id).split('-')[0]

    def getSuffix(self):
	zuser = str(self.principal.id).split('-')
	if len(zuser) == 2:
	    return zuser[1]
	return '00'    

    def getAdresse(self):
	mnr = self.getHauptUser()
	return { 'name1': 'Novareto GmbH',
	         'name2': 'Geschaeftsprozesse im Netz',
		 'name3': '',
		 'strasse': 'Karolinenstr.',
		 'nr': '17',
		 'plz': '91471',
		 'ort': 'Illesheim',
		 'mnr': mnr,
	       }

