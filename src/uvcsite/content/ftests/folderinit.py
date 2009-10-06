"""
ProductFolder is a Utility
==========================

All our ProductFolder are at the same time utilitys

  >>> from zope.app.testing.functional import getRootFolder
  >>> app = App()
  >>> root = getRootFolder()
  >>> root['app'] = app

  >>> import zope.app.appsetup.interfaces
  >>> grok.notify(zope.app.appsetup.interfaces.IDatabaseOpenedWithRootEvent)
  >>> from zope.component import getUtilitiesFor
  >>> from uvcsite.content import IProductFolder
  >>> utils = list(getUtilitiesFor(IProductFolder))

  >>> titles = [x[0] for x in utils]
  >>> 'ENW1Container' in titles 
  True
"""

import grok
from uvcsite.app import Uvcsite
from uvcsite.content import ProductFolder, contenttype

class App(Uvcsite):
    pass


class MyContent(grok.Model):
    """ """


class ENW1Container(ProductFolder):
    grok.name('ENW1Container')
    grok.title('This is a Lastschrift Container')
    grok.description('This is the Description')
    contenttype(MyContent)
