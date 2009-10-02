"""

  >>> from zope.component import getUtilitiesFor
  >>> from uvcsite.content import IProductFolder
  >>> list(getUtilitiesFor(IProductFolder))
  [(u'In diesem Ordner finden Sie Hilfe Dokumente', <class 'uvcsite.helpsystem.folder.HelpFolder'>)]

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


