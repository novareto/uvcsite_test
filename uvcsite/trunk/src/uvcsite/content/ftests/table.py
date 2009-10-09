"""
Check the dynamic table elements in the view of the productfolder 
=================================================================

Setup
-----

  >>> from zope.app.testing.functional import getRootFolder
  >>> r = getRootFolder()
  >>> r['folder'] = folder = Folder()
  >>> folder
  <uvcsite.content.ftests.table.Folder object at ...> 

  >>> print folder.title
  This is a Folder 

  >>> content1 = MyContent()
  >>> content1
  <uvcsite.content.ftests.table.MyContent ...>
  >>> folder['mycontent1'] = content1

  >>> content2 = MyContent()
  >>> content2
  <uvcsite.content.ftests.table.MyContent ...>
  >>> folder['mycontent2'] = content2

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

So if we render we should see our two content objects in the tbody
of our table
  
  >>> print view.render()
  <form...
    <tbody>
      <tr class="even">
        <td><input type="checkbox" class="checkbox-widget" name="deleteFormTable-checkBox-0-selectedItems" value="mycontent1"  /></td>
        <td><a href="http://127.0.0.1/folder/mycontent1/edit"></a></td>
        <td>MyContent</td>
        <td>Entwurf</td>
        <td></td>
        <td>...</td>
      </tr>
      <tr class="odd">
        <td><input type="checkbox" class="checkbox-widget" name="deleteFormTable-checkBox-0-selectedItems" value="mycontent2"  /></td>
        <td><a href="http://127.0.0.1/folder/mycontent2/edit"></a></td>
        <td>MyContent</td>
        <td>Entwurf</td>
        <td></td>
        <td>...</td>
      </tr>
    </tbody>
  ...
  </form>

View with content in the Workflow Status gesendet
-------------------------------------------------

We fire publish the content1 object. 

  >>> from hurry.workflow.interfaces import IWorkflowInfo
  >>> IWorkflowInfo(content1).fireTransition('publish')

Objects in the publish status can not be deleted so the
checkbox is gone. And the link does not point on the
edit action it now points on the view action.

  >>> print view.render()
  <form...
    <tbody>
      <tr class="even">
        <td></td>
        <td><a href="http://127.0.0.1/folder/mycontent1"></a></td>
        <td>MyContent</td>
        <td>gesendet</td>
        <td></td>
        <td>...</td>
      </tr>
      <tr class="odd">
        <td><input type="checkbox" class="checkbox-widget" name="deleteFormTable-checkBox-0-selectedItems" value="mycontent2"  /></td>
        <td><a href="http://127.0.0.1/folder/mycontent2/edit"></a></td>
        <td>MyContent</td>
        <td>Entwurf</td>
        <td></td>
        <td>...</td>
      </tr>
    </tbody>
  ...
  </form>

"""
import grok

from megrok import z3cform
from megrok import layout
from zope.interface import Interface
from zope.schema import TextLine, Int
from uvcsite.content import ProductFolder, contenttype, Content, schema

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


class Folder(ProductFolder):
    grok.name('LastschriftContainer3')
    grok.title('This is a Folder')
    grok.description('This is the Description')
    contenttype(MyContent)
