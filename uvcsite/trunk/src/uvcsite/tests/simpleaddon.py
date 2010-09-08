import grok
import uvcsite
import uvc.layout
import zope.schema
import zope.interface
import zope.component


from megrok import navigation
from uvc.validation import validation

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
        constraint = validation.validateZahl
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


class Stat(uvcsite.Page):
    grok.name('stat')
    grok.title('Statistik')
    grok.context(AdressBook)
    uvcsite.sectionmenu(uvcsite.IExtraViews)

    def render(self):
        return "Statistiks"


@grok.subscribe(Contact, uvcsite.IAfterSaveEvent)
def handle_save(obj, event):
    print "AfterSaveEvent"


class AddMenuEntry(grok.View):
    grok.name('Buddy erstellen')
    grok.title('Buddy erstellen')
    grok.context(zope.interface.Interface)
    navigation.sitemenuitem(uvcsite.IGlobalMenu)

    def render(self):
        adapter = zope.component.getMultiAdapter((self.request.principal, self.request), uvcsite.IGetHomeFolderUrl)
        return self.response.redirect(adapter.getAddURL(Contact))
