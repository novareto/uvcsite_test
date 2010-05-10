"""
ProductFolder
=============

The Good Way
------------

First start with makeing an instance of the Container/Folder

  >>> from zope.app.testing.functional import getRootFolder
  >>> root = getRootFolder()

  >>> pf = LastschriftContainer2()
  >>> pf
  <uvcsite.content.ftests.persistent.LastschriftContainer2 object at ...>

  >>> root['pf'] = pf
  >>> from zope.component import getMultiAdapter
  >>> from zope.publisher.browser import TestRequest


  >>> view = getMultiAdapter((pf, TestRequest()), name=u"add")
  >>> print view.render()
  Yes

"""

import grok
from uvcsite.content import ProductFolder, contenttype


class MyContent(grok.Model):
    """ """


class LastschriftContainer2(ProductFolder):
    grok.name('LastschriftContainer2')
    grok.title('This is a Lastschrift Container')
    grok.description('This is the Description')
    contenttype(MyContent)


class Add(grok.View):
    grok.context(LastschriftContainer2)

    def render(self):
	return "Yes"

