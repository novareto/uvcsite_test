from zope.schema import TextLine
from zope.interface import Interface

class IUVCAuth(Interface):
    
    prefix = TextLine( title=u'Prefix',
                       description=u'Prefix',
                       missing_value=u'',
                       default=u'',
                     )

class IMasterUser(Interface):
    """ Marker Interface for MasterUser"""
