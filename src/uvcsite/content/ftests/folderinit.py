"""
Event which set's all the ProductFolders
========================================

Setup
-----

  >>> import grok
  >>> from zope.app.testing.functional import getRootFolder
  >>> from zope.app.publication.zopepublication import ZopePublication

Before we fire up the DatabaseOpendEvent we have to prepare a ZODB

  >>> from ZODB.tests.util import DB
  >>> from zope.app.appsetup import bootstrap
  >>> import zope.processlifetime
  >>> from zope.app.component.hooks import getSite, setSite
    
  >>> db = DB()
  >>> bootstrap.bootStrapSubscriber(zope.processlifetime.DatabaseOpened(db))
  >>> conn = db.open()
  >>> root = conn.root()

Let's put our app in the ZODB

  >>> app = App()
  >>> app
  <uvcsite.content.ftests.folderinit.App object at ...>

  >>> root[ZopePublication.root_name]['app'] = app
  >>> setSite(root[ZopePublication.root_name]['app'])

We need an empty HomeFolder for checking if the assigment of
our Product folders work. This means i add the user lars to
the HomeFolderManager

  >>> from zope.component import getUtility
  >>> from zope.app.homefolder.interfaces import IHomeFolderManager
  >>> utility = getUtility(IHomeFolderManager)
  >>> utility
  <uvcsite.homefolder.homefolder.PortalMembership object at ...>

We create an empty HomeFolder for lars:

  >>> utility.assignHomeFolder('lars')
  >>> 'lars' in utility.homeFolderBase
  True

Let's check that this container is empty: 

  >>> lars = utility.homeFolderBase['lars']
  >>> [x for x in lars] 
  []

  >>> import transaction
  >>> #transaction.commit()

Let's call the event and look if it get called
----------------------------------------------

  >>> import zope.app.appsetup.interfaces
  >>> grok.notify(zope.app.appsetup.interfaces.DatabaseOpenedWithRoot(db))

Ok the event is fired up. Now we should found our ENW1Container in 
the HomeFolder of Lars.

  >>> lars = utility.homeFolderBase['lars']
  >>> 'ENW1Container' in lars 
  True

  >>> 'NotInHomeFolder' not in lars
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


class NotInHomeFolder(ProductFolder):    
    grok.name('NotInHomeFolder')
    grok.title('This should not go into the HomeFolder')
    grok.description('This is the Description')
    contenttype(MyContent)

    inHomeFolder = False 
