"""
ProductFolder
=============

The Good Way
------------

First start with makeing an instance of the Container/Folder

  >>> from zope.component import getUtilitiesFor
  >>> from uvcsite.content import IProductFolder
  >>> list(getUtilitiesFor(IProductFolder))
  [...(u'ENWContainer', <class 'uvcsite.content.ftests.utility.ENWContainer'>)...]

"""

import grok
from uvcsite.content import ProductFolder, contenttype


class MyContent(grok.Model):
    """ """


class ENWContainer(ProductFolder):
    grok.name('ENWContainer')
    grok.title('This is a Lastschrift Container')
    grok.description('This is the Description')
    contenttype(MyContent)

