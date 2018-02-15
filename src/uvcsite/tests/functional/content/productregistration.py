"""
Functional Doctest
==================

:Test-Layer: functional

  >>> import grok
  >>> grok.grok('uvcsite.tests.functional.content.productregistration')

  >>> import uvcsite
  >>> from uvcsite.app import Uvcsite
  >>> from zope.pluggableauth.factories import Principal
  >>> from zope.publisher.browser import TestRequest
  >>> from zope.component import getUtility, getMultiAdapter, queryMultiAdapter, getAdapters
  >>> from uvcsite.content.interfaces import IProductRegistration
  >>> from uvcsite.content.directive import productfolder 
  >>> from uvcsite.content.productregistration import ProductRegistration
  >>> from zope.app.homefolder.interfaces import IHomeFolderManager
  >>> from zope.component.hooks import setSite
  >>> import zope.security.management


  >>> root = getRootFolder()
  >>> root['app'] = app = Uvcsite()
  >>> setSite(app)

  >>> root['app']
  <uvcsite.app.Uvcsite object at ...>

  >>> utility = getUtility(IHomeFolderManager)
  >>> christian = Principal('christian', 'christian')
  >>> christian
  Principal('christian')

  >>> request = TestRequest()
  >>> request.setPrincipal(christian)
  >>> zope.security.management.newInteraction(request)

  >>> utility.assignHomeFolder('christian')

  >>> regs = dict([x for x in getAdapters((christian, request), IProductRegistration)])
  >>> adr = regs['adressbook']
  >>> adr 
  <...Addressbook object at ...>

  >>> adr.folderURI
  'Adressbook'

  >>> adr.linkname
  'Adressbuch'

  >>> adr.rolename
  'Adressbuch'

  >>> adr.productfolder
  <class 'uvcsite.tests.fixtures.simpleaddon.AdressBook'>

  >>> homefolder = uvcsite.getHomeFolder(request)
  >>> [x for x in homefolder.keys()]
  [u'Adressbook']

  >>> adr.createInProductFolder()

  >>> [x for x in homefolder.keys()]
  [u'Adressbook']

  >>> len(list(getAdapters((christian, request), IProductRegistration)))
  2

  >>> uaz_registration = getMultiAdapter(
  ...     (christian, request), IProductRegistration, name="Unfallanzeige")
  >>> uaz_registration
  <...UAZRegistration object at ...>

  >>> zope.security.management.endInteraction()


CUSTOM GROUP
------------

  >>> from zope.interface import Interface, alsoProvides

  >>> lars = Principal('lars', 'lars')
  >>> alsoProvides(lars, ISpecialPrincipal)
  >>> lars 
  Principal('lars')

  >>> request = TestRequest()
  >>> request.setPrincipal(lars)
  >>> zope.security.management.newInteraction(request)
  >>> uaz_reg = getMultiAdapter(
  ...     (lars, request), IProductRegistration, name="Unfallanzeige")
  >>> uaz_reg
  <...UAZRegistration object at ...>



  >>> spe_uaz_reg = getMultiAdapter((lars, request), IProductRegistration, name="Unfallanzeige")
  >>> spe_uaz_reg
  <...SpecialUAZRegistration object at ...>

  >>> spe_uaz_reg is not uaz_reg
  True

  >>> spe_uaz_reg.title
  'Spezial Unfallanzeige'

  >>> uvcsite.getProductRegistrations()
  [(u'adressbook', <...Addressbook object at ...>)]

  >>> uvcsite.getAllProductRegistrations()
  [(u'adressbook', <...Addressbook object at ...>),
   (u'Unfallanzeige', <...SpecialUAZRegistration object at ...)]

  >>> zope.security.management.endInteraction()
"""

import grok
from zope.interface import Interface
from uvcsite.content.directive import productfolder 
from uvcsite.content.productregistration import ProductRegistration
from zope.publisher.interfaces.http import IHTTPRequest


class ISpecialPrincipal(Interface):
    """ MARKER """


class Addressbook(ProductRegistration):
    grok.name('adressbook')
    grok.title('Adressbuch')
    grok.description('Beschreibung Entgeltnachweis')
    productfolder('uvcsite.tests.fixtures.simpleaddon.AdressBook')


class UAZRegistration(ProductRegistration):
    grok.name('Unfallanzeige')
    grok.title('Unfallanzeige')
    grok.description('Elektronische Unfallanzeige')


class SpecialUAZRegistration(UAZRegistration):
    grok.adapts(ISpecialPrincipal, IHTTPRequest)
    grok.title('Spezial Unfallanzeige')
