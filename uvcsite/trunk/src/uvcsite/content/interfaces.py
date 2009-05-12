from zope.interface import Interface, invariant, Invalid
from zope.schema import TextLine
from uvcsite.interfaces import IContentType


class IPerson(IContentType):
    """   """

    name = TextLine(title=u"Name", min_length=5)
    vorname = TextLine(title=u"Vorname") 

    @invariant
    def sameNames(person):
	if person.name == person.vorname:
	    raise Invalid("Same Name for name and vorname")
