"""
:doctest:
:layer: uvcsite.tests.FunctionalLayer

Rest API
========

Setup
-----
First start with an instance of UAZFolder

  >>> import grok
  >>> grok.grok('uvcsite.content.ftests.api')

  >>> from zope.app.testing.functional import getRootFolder
  >>> root = getRootFolder()

  >>> from uvcsite.content.ftests.api import UAZFolder
  >>> folder = UAZFolder()
  >>> folder
  <uvcsite.content.ftests.api.UAZFolder object at ...>

Add the folder to the RootFolder!

  >>> root['uaz'] = folder
  >>> root['uaz']
  <uvcsite.content.ftests.api.UAZFolder object at ...>

Rest Operations
---------------

  >>> from uvcsite.content.ftests import http_call

POST
----

Ok there is no meaningful post method implemented yet!

  >>> auth_header="Basic uaz:uaz"

GET
---

So start with a GET Request of the Container! Ok are no
content objects in it so we only get an empty container listing.

  >>> response = http_call('GET', 'http://localhost/++rest++api/uaz', AUTHORIZATION=auth_header)
  >>> print response.getBody()
  <?xml version='1.0' encoding='utf-8'?>
  <container id="uaz"/>

Now let's add objects to the container and see the GET Request again

  >>> from uvcsite.content.ftests.api import Unfallanzeige
  >>> uaz = Unfallanzeige()
  >>> uaz.title = u"Mein Unfall"
  >>> uaz.name = u"Christian Klinger"
  >>> uaz.age = 29

  >>> uaz1 = Unfallanzeige()
  >>> uaz1.title = u"Unfall von Lars"
  >>> uaz1.name = u"Lars Walther"
  >>> uaz1.age = 39

One item in the container!

  >>> root['uaz']['christian'] = uaz
  >>> response = http_call('GET', 'http://localhost/++rest++api/uaz',
  ... AUTHORIZATION=auth_header)
  >>> print response.getBody()
  <?xml version='1.0' encoding='utf-8'?>
  <container id="uaz">
    <Unfallanzeige>
      <id>christian</id>
      <titel>Mein Unfall</titel>
      <author>uvc.uaz</author>
      <datum>...</datum>
      <status>Entwurf</status>
    </Unfallanzeige>
  </container>

The object itself has also a get method

  >>> response = http_call('GET', 'http://localhost/++rest++api/uaz/christian',
  ... AUTHORIZATION=auth_header)
  >>> print response.getBody()
  <?xml version='1.0' encoding='UTF-8'?>
  <unfallanzeige id="christian">
    <Unfallanzeige id="christian">
      <title>Mein Unfall</title>
      <name>Christian Klinger</name>
      <age>29</age>
    </Unfallanzeige>
  </unfallanzeige>
  <BLANKLINE>


More items in the container!

  >>> root['uaz']['lars'] = uaz1
  >>> response = http_call('GET', 'http://localhost/++rest++api/uaz',
  ... AUTHORIZATION=auth_header)
  >>> print response.getBody()
  <?xml version='1.0' encoding='utf-8'?>
  <container id="uaz">
    <Unfallanzeige>
      <id>christian</id>
      <titel>Mein Unfall</titel>
      <author>uvc.uaz</author>
      <datum>...</datum>
      <status>Entwurf</status>
    </Unfallanzeige>
    <Unfallanzeige>
      <id>lars</id>
      <titel>Unfall von Lars</titel>
      <author>uvc.uaz</author>
      <datum>...</datum>
      <status>Entwurf</status>
    </Unfallanzeige>
  </container>



PUT
---

A Valid uaz_xml file!

  >>> uaz_xml = '''
  ...    <Unfallanzeige id="christian">
  ...      <title>Unfallmeldung</title>
  ...      <name>Christian Moser</name>
  ...      <age>30</age>
  ...    </Unfallanzeige>'''
  >>> response = http_call('PUT', 'http://localhost/++rest++api/uaz', uaz_xml,
  ... AUTHORIZATION=auth_header)
  CALLED: After Save Event
  >>> print response.getBody()
  <success id="Unfallanzeige" name="Unfallanzeige"/>

We should get this document in our container

  >>> uaz = root['uaz']['Unfallanzeige']
  >>> uaz
  <uvcsite.content.ftests.api.Unfallanzeige object at ...>

  >>> print uaz.name
  Christian Moser

  >>> print uaz.age
  30

We should now have 3 objects in our container!

  >>> len(root['uaz'])
  3

An Invalid uaz_xml file!

  >>> uaz_xml_with_error = '''
  ...    <Unfallanzeige id="christian">
  ...      <title>Mein Unfall</title>
  ...      <name>Christian Klinger Junior</name>
  ...      <age>twenty nine</age>
  ...    </Unfallanzeige>'''
  >>> response = http_call('PUT', 'http://localhost/++rest++api/uaz',
  ... uaz_xml_with_error, AUTHORIZATION=auth_header)

  >>> result = response.getBody()
  >>> expected_result = '''
  ... <failure>
  ...   <error field="age" message="Inappropriate argument value (of correct type)."><age>twenty nine</age>
  ...   </error>
  ...  <error field="name" message="Value is too long"><name>Christian Klinger Junior</name>
  ...     </error>
  ... </failure>'''

  >>> from lxml import etree
  >>> from formencode.doctest_xml_compare import xml_compare
  >>> tree1 = etree.fromstring(result.strip())
  >>> tree2 = etree.fromstring(expected_result.strip())
  >>> assert xml_compare(tree1,tree2) is False  # identical.


An invariant uaz_xml file

  >>> uaz_xml_with_invariant = '''
  ...    <Unfallanzeige id="christian">
  ...      <title>Mein Unfall</title>
  ...      <name>hans</name>
  ...      <age>10</age>
  ...    </Unfallanzeige>'''
  >>> response = http_call('PUT', 'http://localhost/++rest++api/uaz',
  ...  uaz_xml_with_invariant, AUTHORIZATION=auth_header)
  >>> print response.getBody()
  <failure>
    <error text="Invariant: This combination of name and age is not valid"/>
  </failure>

"""

import grok
import uvcsite.tests
from uvcsite.content import ProductFolder, IContent, Content, schema, name, contenttype
from zope.schema import TextLine, Int
from zope.interface import Invalid, invariant
from dolmen import content


class IUnfallanzeige(IContent):
    name = TextLine(title = u"Name", max_length=20)
    age = Int(title = u"Int")

    @invariant
    def no_sample(unfallanzeige):
        if unfallanzeige.name == "hans" and unfallanzeige.age == 10:
            raise Invalid("This combination of name and age is not valid")


class Unfallanzeige(Content):
    grok.implements(IUnfallanzeige)
    grok.name('Unfallanzeige')
    content.schema(IUnfallanzeige)


class UAZFolder(ProductFolder):
    contenttype(Unfallanzeige)


@grok.subscribe(Unfallanzeige, uvcsite.IAfterSaveEvent)
def handle_save_print(event, obj):
    print "CALLED: After Save Event"
