import grok
import uvcsite
import uvc.layout
import zope.schema
import zope.interface
import zope.component

from dolmen import menu
from megrok import navigation
from uvc.validation import validation
from hurry.workflow.interfaces import IWorkflowInfo


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



class IAdressBook(uvcsite.IProductFolder):
    """ Marker Interface """


class Contact(uvcsite.Content):
    grok.implements(IContact)
    grok.name(u'Kontakt')
    uvcsite.schema(IContact)


class AdressBook(uvcsite.ProductFolder):
    grok.implements(IAdressBook)
    grok.name('adressbook')
    grok.title('Adressbuch')
    grok.description('Adressbuch ...')
    uvcsite.contenttype(Contact)



class ADMenu(grok.Viewlet):
    grok.viewletmanager(uvcsite.IAboveContent)
    grok.context(AdressBook)
    grok.order(40)

    def render(self):
        url = self.view.url(self.context, 'stat')
        return "<dl class='dropdown'> <dt> <a href=%s> Alte Dokumente </a> </dt> </dl>" % url



#@menu.menuentry(uvcsite.IExtraViews)
class Stat(uvcsite.Page):
    grok.name('stat')
    grok.title('Statistik')
    grok.context(AdressBook)
    uvcsite.sectionmenu(uvcsite.IExtraViews)

    def render(self):
        return "<div> <h1>Statistiks</h1> </div>"


@grok.subscribe(Contact, uvcsite.IAfterSaveEvent)
def handle_save(obj, event):
    try:
        1/0
        IWorkflowInfo(obj).fireTransition('publish')
    except StandardError, e:
        IWorkflowInfo(obj).fireTransition('progress')
        uvcsite.log('simpleaddon', e.__doc__)
    print "AfterSaveEvent"


class AddMenuEntry(grok.View):
    grok.name('Buddy erstellen')
    grok.title('Buddy erstellen')
    grok.context(zope.interface.Interface)
    navigation.sitemenuitem(uvcsite.IGlobalMenu)

    def render(self):
        adapter = zope.component.getMultiAdapter((self.request.principal, self.request), uvcsite.IGetHomeFolderUrl)
        return self.response.redirect(adapter.getAddURL(Contact))

def kopf(c):
    c.drawString(200,200, u"Ich bin der KOPF")

class KontaktPdf(uvcsite.BasePDF):
    grok.context(IContact)
    grok.name('pdf')

    def genpdf(self):
        c = self.c
        kopf(c)
        c.drawString(100,100, "Hello World")
        c.drawString(300,300, self.request.principal.id)
        c.showPage()
