"""

  >>> from zope.component import getUtilitiesFor
  >>> from uvcsite.content import IProductFolder
  >>> utils = list(getUtilitiesFor(IProductFolder))
  >>> titles = [x[0] for x in utils]
  >>> 'ENW1Container' in titles 
  True
"""

import grok
from uvcsite.content import ProductFolder, contenttype

class App(grok.Application):
    pass


class MyContent(grok.Model):
    """ """


class ENW1Container(ProductFolder):
    grok.name('ENW1Container')
    grok.title('This is a Lastschrift Container')
    grok.description('This is the Description')
    contenttype(MyContent)


