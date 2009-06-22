# -*- coding: utf-8 -*- 
# Copyright (c) 2007-2008 NovaReto GmbH 
# cklinger@novareto.de 

import grok
from zope.interface import Interface
from uvcsite.api.interfaces import ICompanyInfo, ICompanyAddress
from zope.app.authentication.interfaces import IPrincipal

class CompanyInfo(grok.Adapter):
    """ Adapter for General Company Things"""
    grok.implements(ICompanyInfo)
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

class CompanyAddress(grok.Adapter):
    """ Adapter for Company Adress"""
    grok.implements(ICompanyAddress)
    grok.context(IPrincipal)

    def getAddress(self):
	return { 'name1': 'Novareto GmbH',
	         'name2': 'Geschaeftsprozesse im Netz',
		 'name3': '',
		 'strasse': 'Karolinenstr.',
		 'nr': '17',
		 'plz': '91471',
		 'ort': 'Illesheim',
		 'mnr': '0101010001',
	       }

