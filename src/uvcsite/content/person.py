import grok
from megrok.pagelet.component import FormPageletMixin

from hurry.workflow.interfaces import IWorkflowInfo
from uvcsite.app import Uvcsite
from interfaces import IPerson
from zope.interface import implementedBy
from zope.component import getUtility, createObject
from zope.component.interfaces import IFactory
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.app.homefolder.interfaces import IHomeFolderManager
from zope.securitypolicy.interfaces import IPrincipalRoleMap
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.schema.fieldproperty import FieldProperty


from zope.securitypolicy.interfaces import IPrincipalPermissionManager

### Factory

class PersonFactory(grok.GlobalUtility):
    grok.implements(IFactory)
    grok.name('uvc.Person')

    title = u"Create a new Person"
    descritpin = u"This factory instaciates new persons"

    def __call__(self):
	person = Person()
	grok.notify(grok.ObjectCreatedEvent(person))
	return person 

    def getInterfaces(self):
	return implementedBy(Person)

### Die Person Klasse
class Person(grok.Model):
    meta_type = 'Person'
    grok.implements(IPerson)

    name = FieldProperty(IPerson['name'])
    vorname = FieldProperty(IPerson['vorname'])


### Die Person View Form
class PersonIndex(FormPageletMixin, grok.DisplayForm):
    grok.context(Person)
    grok.name('index')
    grok.require('uvc.CanViewKontakt')
    form_fields = grok.Fields(IPerson)
    template = grok.PageTemplateFile('display_form.pt')

    def update(self):
	prm = IPrincipalRoleMap(self.context)
	print prm.getRolesForPrincipal(self.request.principal.id)


### Die Person Add Form
class PersonAdd(FormPageletMixin, grok.AddForm):
    grok.context(Uvcsite)
    grok.require('uvc.CanAddKontakt')
    template = grok.PageTemplateFile('form.pt')
    form_fields = grok.Fields(IPerson)

    @grok.action(u'Anlegen')
    def addThisShit(self, **kw):
	person = createObject(u"uvc.Person") 
	self.applyData(person, **kw)
	principal = self.request.principal    
	utility = getUtility(IHomeFolderManager)
	homeFolder = utility.getHomeFolder(str(principal.id))
	id = "%s-%s" %(kw.get('name'), len(homeFolder))

	homeFolder[id] = person
	#print "Setting Edit Permission for the User", self.request.principal.id
	permission_man = IPrincipalPermissionManager(person)
	permission_man.grantPermissionToPrincipal( 'uvc.CanEditKontakt', self.request.principal.id)
	permission_man.grantPermissionToPrincipal( 'uvc.CanViewKontakt', self.request.principal.id)
	#self.redirect(self.url(person))


### Die Person Edit Form
class PersonEdit(FormPageletMixin, grok.EditForm):
    grok.context(Person)
    grok.name('edit')
    grok.require('uvc.CanEditKontakt')
    template = grok.PageTemplateFile('form.pt')
    form_fields = grok.Fields(IPerson)


    @grok.action(u'Speichern')
    def finishWorkflow(self, **data):
	IWorkflowInfo(self.context).fireTransition('publish')

    @grok.action(u'ROLLENCHEKC')
    def do_the_role_dance(self, **data):
	person = self.context
	permission_man = IPrincipalPermissionManager(person)
	permission_man.denyPermissionToPrincipal( 'uvc.CanEditKontakt', self.request.principal.id)
	self.redirect(self.url(person))
	

### Menus
from uvcsite.viewlets.managers import Sidebar
from z3c.menu.simple.menu import GlobalMenuItem
from zope.interface import Interface

class Beispiel(grok.Viewlet, GlobalMenuItem):
    """ Image Things"""
    grok.name('Kontakt')
    grok.context(Interface)
    grok.viewletmanager(Sidebar)

    urlEndings = "personadd"
    viewURL = "personadd"

    def render(self):
        return self.template()
	
