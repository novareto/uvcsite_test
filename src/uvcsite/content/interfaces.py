from zope.schema import DottedName
from zope.interface import Interface
from grok.interfaces import IContainer


class IUVCApplication(Interface):
    """ Marker Interface the application_url method """


class IProductFolder(IContainer):
    """ MARKER"""


class IFolderColumnTable(Interface):
    """ Provide standard folder columns"""

