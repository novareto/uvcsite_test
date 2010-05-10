"""
ProductFolder
=============

The Good Way
------------

First start with makeing an instance of the Container/Folder
  >>> from grok.testing import grok
  >>> grok(__name__)
  >>> pf = LastschriftContainer1()
  >>> pf
  <uvcsite.content.ftests.container.LastschriftContainer1 object at ...>

We should now get properties for name, title and description

name

  >>> print pf.name
  LastschriftContainer1

title

  >>> print pf.title
  This is a Lastschrift Container

description

  >>> print pf.description
  This is the Description

And we should get back our class with the get ContentType method

  >>> pf.getContentType()
  <class 'uvcsite.content.ftests.container.MyContent'>


The not so Good Way
-------------------

   >>> uc = UnfallanzeigeContainer1()

We don't give a name, title and description

   >>> uc.name
   u''

   >>> uc.title

   >>> uc.description
"""

import grok
from uvcsite.content import ProductFolder, contenttype


class MyContent(grok.Model):
    """ """


class LastschriftContainer1(ProductFolder):
    grok.name('LastschriftContainer1')
    grok.title('This is a Lastschrift Container')
    grok.description('This is the Description')
    contenttype(MyContent)


class UnfallanzeigeContainer1(ProductFolder):
    contenttype(MyContent)

