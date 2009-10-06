import grok

from megrok import z3ctable
from megrok.z3cform import base as z3cform
from uvcsite.content import IProductFolder, ApplicationAwareView
from z3c.form import form
#from uvcsite.skin.skin import Scripts
from megrok.z3cform.tabular import DeleteFormTablePage
from uvcsite.content import ApplicationAwareView

class Index(DeleteFormTablePage, ApplicationAwareView):
    grok.context(IProductFolder)

    cssClasses = {'table': 'tablesorter myTable'}
    cssClassEven = u'even'
    cssClassOdd = u'odd'

    def executeDelete(self, item):
        self.flash(u'Ihre Dokumente wurden entfernt')
        del item.__parent__[item.__name__]


class Add(z3cform.PageAddForm, ApplicationAwareView):
    grok.context(IProductFolder)
    grok.require('uvc.AddContent')

    @property
    def fields(self):
	fields = z3cform.meta.get_auto_fields(self.context.getContentType())
	return z3cform.Fields(fields)

    def create(self, data):
        content = self.context.getContentType()()
        form.applyChanges(self, content, data)
        return content 

    def add(self, content):
        self.context.add(content)

    def nextURL(self):
        self.flash('Added Content')
        return self.url(self.context) 
