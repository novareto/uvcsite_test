import grok
import uvcsite
import uvc.layout
import zope.schema
import zope.interface
import zope.component
from uvc.layout.directives import bound_resource

class ErrorDateFields(zope.interface.Invalid):
    """Fehlerklasse """


class IContact(uvcsite.IContent):

    name = zope.schema.TextLine(
        title = u"Name",
        description = u"Wie ist ihr Name",
        )

    alter = zope.schema.TextLine(
        title = u"Alter",
        description = u"Wie ist ihr Alter",
        )

    @zope.interface.invariant
    def validate(obj):
        if obj.name != "christian":
            raise ErrorDateFields("klaus")



class IAdressBook(uvcsite.IProductFolder):
    """ Marker Interface """


class Contact(uvcsite.Content):
    grok.name(u'Kontakt')
    uvcsite.schema(IContact)


class AdressBook(uvcsite.ProductFolder):
    grok.name('adressbook')
    grok.title('Adressbook')
    grok.description('Description of Adressbook')
    uvcsite.contenttype(Contact)


@bound_resource('entgelt.jpg', name="uvc.tests.entgelt")
class AddMenuEntry(uvcsite.Entry):
    grok.name('Buddy erstellen')
    grok.title('Buddy erstellen')
    grok.context(zope.interface.Interface)
    uvcsite.menu(uvcsite.GlobalMenu)
    uvc.layout.menus.category(u'Apps')

    @property
    def url(self):
        adapter = zope.component.getMultiAdapter((self.request.principal, self.request), uvcsite.IGetHomeFolderUrl)
        return adapter.getAddURL(Contact)
