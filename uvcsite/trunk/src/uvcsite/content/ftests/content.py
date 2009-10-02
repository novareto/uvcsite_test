"""
Content
=======

Setup
-----
First start with makeing an instance of the Content 

  >>> content = MyContent() 
  >>> content 
  <uvcsite.content.ftests.content.MyContent object at ...> 

Attributes
----------
There should be the two attributes from our IContent Schema

  >>> content.name

  >>> content.age


Schema
------

  >>> content.schema
  [<InterfaceClass uvcsite.content.ftests.content.IContent>] 

Icon
----

  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest
  >>> icon_view = getMultiAdapter((content, TestRequest()),  name="contenttype_icon")
  >>> print icon_view()
  <img src="http://127.0.0.1/@@/uvcsite-content-ftests-content-IContent-contenttype_icon.png" alt="Content" width="16" height="16" border="0" />

BaseClasses
-----------

  >>> from uvcsite.content.components import Content, ProductFolder

  >>> content = Content()
  >>> content.schema
  [<InterfaceClass dolmen.content.interfaces.IBaseContent>] 

  >>> print content.meta_type
  Content

"""

import grok
from uvcsite.content import IContent, Content, schema, name 
from zope.schema import TextLine, Int

class IContent(IContent):
    name = TextLine(title = u"Name")
    age = Int(title = u"Int")


class MyContent(Content):
    grok.implements(IContent)
    schema(IContent)
    name('MyContent')


