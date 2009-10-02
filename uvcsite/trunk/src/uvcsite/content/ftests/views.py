"""
The Default Views of the ProductFolder
======================================

Setup
-----

  >>> from zope.app.testing.functional import getRootFolder
  >>> r = getRootFolder()
  >>> r['pf'] = pf = LastschriftContainer3()
  >>> pf
  <uvcsite.content.ftests.views.LastschriftContainer3 object at ...> 

  >>> print pf.title
  This is a Lastschrift Container

  >>> mycontent = MyContent()
  >>> mycontent
  <uvcsite.content.ftests.views.MyContent ...>

  >>> pf['mycontent'] = mycontent

Views
-----

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

Get the ViewClass

  >>> view = getMultiAdapter((pf, request), name=u"index")
  >>> view.update() 
  >>> view
  <Index 'index'>

Render the ViewClass
Note: There are default columns defined for IContainer in
      uvcsite so. No need here to define Columns
  
  >>> print view.render()
  <form action="http://127.0.0.1" method="post"
        enctype="multipart/form-data" class="edit-form"
        name="deleteFormTable" id="deleteFormTable">
    <div class="viewspace">
      <div>
      <div class="tabluarTable">
      </div>
      <div class="tabluarForm">
      </div>
    </div>
    </div>
    <div>
      <div class="buttons">
  <input id="deleteFormTable-buttons-delete"
         name="deleteFormTable.buttons.delete"
         class="submit-widget button-field" value="Delete"
         type="submit" />
      </div>
    </div>
  </form>

If we call this class we should see our tableform in our simple Layout:

  >>> print view()
  <html>
  <form action="http://127.0.0.1" method="post"
        enctype="multipart/form-data" class="edit-form"
        name="deleteFormTable" id="deleteFormTable">
    <div class="viewspace">
      <div>
      <div class="tabluarTable">
      </div>
      <div class="tabluarForm">
      </div>
    </div>
    </div>
    <div>
      <div class="buttons">
  <input id="deleteFormTable-buttons-delete"
         name="deleteFormTable.buttons.delete"
         class="submit-widget button-field" value="Delete"
         type="submit" />
      </div>
    </div>
  </form>
  </html>


Add View
--------

Let's check if our default AddForm works for our ProductFolder.
Setting up some basic stuff for working with the testbrowser:

  >>> from zope.app.testing.functional import getRootFolder
  >>> root = getRootFolder()
  >>> root['pf1'] = pf
  >>> from zope.testbrowser.testing import Browser
  >>> browser = Browser()
  >>> browser.handleErrors = False 
  >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')

We call the add form:
  
  >>> browser.open('http://localhost/pf1/add')
  >>> print browser.headers['Status'].upper()
  200 OK

We have a form in our add form:

  >>> form = browser.getForm()
  >>> form.getControl(name='form.widgets.age').value = '33'
  >>> form.getControl(name='form.widgets.name').value = 'Klaus'
  >>> form.getControl(name='form.widgets.title').value = 'Titel'
  >>> form.submit("Add")
   

The delete methods
------------------

Let's get again the index View of our ProductFolder. 
We should get 'mycontent' as item in the container.

  >>> view = getMultiAdapter((pf, request), name=u"index")
  >>> folder = view.context
  >>> 'mycontent' in folder 
  True

The Index View of the ProductFolder has a executeDelete method
which get's called by the deleteAction of the form. So we test
this here manually.

  >>> view.executeDelete(mycontent)
  >>> 'mycontent' in folder
  False

"""
import grok

from megrok import z3cform
from megrok import layout
from zope.interface import Interface
from zope.schema import TextLine, Int
from uvcsite.content import ProductFolder, contenttype, Content, schema
import z3c.flashmessage.receiver
import z3c.flashmessage.sources

grok.global_utility(z3c.flashmessage.sources.SessionMessageSource,
                    name='session')

grok.global_utility(z3c.flashmessage.receiver.GlobalMessageReceiver)


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


class LastschriftContainer3(ProductFolder):
    grok.name('LastschriftContainer3')
    grok.title('This is a Lastschrift Container')
    grok.description('This is the Description')
    contenttype(MyContent)


