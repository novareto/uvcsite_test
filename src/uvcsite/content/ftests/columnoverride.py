"""
ColumnOverride
==============

Setup
-----

  >>> from zope.app.testing.functional import getRootFolder
  >>> r = getRootFolder()
  >>> r['folder'] = folder = OverrideFolder()
  >>> folder
  <uvcsite.content.ftests.columnoverride.OverrideFolder object at ...> 

Views
-----

This are some imports which helps us to call the IndexTable 
of our folder.

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

Let's call the IndexTable of the folder:

  >>> view = getMultiAdapter((folder, request), name=u"index")
  >>> view.update() 

Instead of the <th>Title<th> we should get <th>OverrideTable</th>:
  
  >>> print view.render()
  <form...
    <thead>
      <tr>
        <th class="checkBox"></th>
        <th>OverrideTitle</th>
        <th>Objekt</th>
        <th>Status</th>
        <th>Autor</th>
        <th>Datum</th>
      </tr>
    </thead>
  ...
  </form>
"""
import grok

from megrok import z3cform
from megrok import layout
from megrok.z3ctable import LinkColumn
from zope.interface import Interface
from zope.schema import TextLine, Int
from uvcsite.content import ProductFolder, contenttype, Content, schema
from uvcsite.interfaces import IFolderColumnTable


class MyLayout(layout.Layout):
    grok.context(Interface)

    def render(self):
	return "<html> %s </html>" %(self.view.render())

class IMyContent(Interface):
    name = TextLine(title = u"Name")
    age = Int(title = u"Age")


class MyContent(Content):
    grok.implements(IMyContent)    
    grok.name('MyContent')
    schema(IMyContent)


class OverrideFolder(ProductFolder):
    grok.name('OverrideFolder')
    grok.title('This is a Folder')
    grok.description('This is the Description')
    contenttype(MyContent)


class OverrideTitleColumn(LinkColumn):
    grok.name('link')
    grok.context(IFolderColumnTable)
    header = u"OverrideTitle"
    weight = 1
    
