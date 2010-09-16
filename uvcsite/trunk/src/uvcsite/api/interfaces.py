# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de

from zope.interface import Interface


class ICompanyInfo(Interface):
    """ A Utlity for getting basic
        data from Companys such as
        address, account information ...
    """

    def getMasterUser(mnr):
        """ Return a dict with Adresse """

    def getSuffix(mnr):
        """ Return the suffix for the User"""


class ICompanyAddress(Interface):
    """ Return the Company Address for a Principal"""

    def getAddress(principal):
        """ Return a dict with the Address
               { 'name1': 'Novareto GmbH',
                 'name2': 'Geschaeftsprozesse im Netz',
                 'name3': '',
                 'strasse': 'Karolinenstr.',
                 'nr': '17',
                 'plz': '91471',
                 'ort': 'Illesheim',
                 'mnr': mnr,}
        """
