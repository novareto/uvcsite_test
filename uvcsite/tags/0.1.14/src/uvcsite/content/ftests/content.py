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
from uvcsite import content
from zope.schema import TextLine, Int

class IContent(content.IContent):
    name = TextLine(title = u"Name")
    age = Int(title = u"Int")


class MyContent(content.Content):
    grok.implements(IContent)
    content.schema(IContent)
    content.name('MyContent')
