from zope.interface import Interface

class ICompanyInfo(Interface):
    """ A Utlity for getting basic 
        data from Companys such as
        address, account information ...
    """

    def getAdresse(mnr):
        """ Return a dict with Adresse """

    def getVeranlagung(mnr):
        """ Return a resultset with veranlagungen"""

