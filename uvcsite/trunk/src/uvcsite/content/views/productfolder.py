import grok
from zope.app import zapi
from uvcsite import IProductFolder
from megrok.z3cform import PageAddForm
from zope.app.homefolder.interfaces import IHomeFolder

class Add(PageAddForm):
    grok.context(IProductFolder)

    @property
    def fields(self):
        return megrok.z3cform.meta.get_auto_fields(self.getContentType())

