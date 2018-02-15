"""
:doctest:
:layer: uvcsite.tests.FunctionalLayer

Rest API
========

Setup
-----
First start with an instance of UAZFolder

  >>> import grok
  >>> grok.grok('uvcsite.tests.functional.content.api_json')

  >>> root = getRootFolder()

  >>> from uvcsite.tests.functional.content.api_json import UAZFolder
  >>> folder = UAZFolder()
  >>> folder
  <uvcsite.tests.functional.content.api_json.UAZFolder object at ...>

Add the folder to the RootFolder!

  >>> root['uaz'] = folder
  >>> root['uaz']
  <uvcsite.tests.functional.content.api_json.UAZFolder object at ...>

Rest Operations
---------------


POST
----

Ok there is no meaningful post method implemented yet!

  >>> auth_header="Basic uaz:uaz"

GET
---

So start with a GET Request of the Container! Ok are no
content objects in it so we only get an empty container listing.

  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++jsonapi/uaz', AUTHORIZATION=auth_header)
  >>> import json
  >>> def format(response):
  ...     return json.dumps(json.loads(response.getBody()), indent=4, sort_keys=True)
  >>> print format(response)
  {
      "id": "uaz",
      "items": []
  }

Now let's add objects to the container and see the GET Request again

  >>> from uvcsite.tests.functional.content.api_json import Unfallanzeige
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
  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++jsonapi/uaz',
  ... AUTHORIZATION=auth_header)
  >>> print format(response)
  {
      "id": "uaz",
      "items": [
          {
              "@url": "http://www.google.de",
              "author": "uvc.uaz",
              "datum": "...",
              "id": "christian",
              "meta_type": "Unfallanzeige",
              "status": "Entwurf",
              "titel": "Mein Unfall"
          }
      ]
  }


The object itself has also a get method

  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++jsonapi/uaz/christian',
  ... AUTHORIZATION=auth_header)
  >>> print format(response)
  {
      "age": 29,
      "name": "Christian Klinger",
      "title": "Mein Unfall"
  }

More items in the container!

  >>> root['uaz']['lars'] = uaz1
  >>> response = http_call(wsgi_app(), 'GET', 'http://localhost/++rest++jsonapi/uaz',
  ... AUTHORIZATION=auth_header)
  >>> print format(response)
  {
      "id": "uaz", 
      "items": [
          {
              "@url": "http://www.google.de", 
              "author": "uvc.uaz", 
              "datum": "...", 
              "id": "christian", 
              "meta_type": "Unfallanzeige", 
              "status": "Entwurf", 
              "titel": "Mein Unfall" 
          },
          {
              "@url": "http://www.google.de", 
              "author": "uvc.uaz", 
              "datum": "...", 
              "id": "lars", 
              "meta_type": "Unfallanzeige", 
              "status": "Entwurf", 
              "titel": "Unfall von Lars" 
          }
      ]
  }



PUT
---

A Valid uaz_xml file!

  >>> uaz_xml = '''
  ...     {
  ...         "age": 30,
  ...         "name": "Christian Moser",
  ...         "title": "Mein Unfall JSON"
  ...      }
  ...    '''
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++jsonapi/uaz', uaz_xml, AUTHORIZATION=auth_header)

  >>> print format(response)
  {
      "id": "Unfallanzeige",
      "name": "Unfallanzeige",
      "result": "success"
  }

We should get this document in our container

  >>> uaz = root['uaz']['Unfallanzeige']
  >>> uaz
  <uvcsite.tests.functional.content.api_json.Unfallanzeige object at ...>

  >>> print uaz.name
  Christian Moser

  >>> print uaz.age
  30

We should now have 3 objects in our container!

  >>> len(root['uaz'])
  3

Invalid uaz_xml file!

  >>> uaz_json_with_error = '''
  ... {
  ...       "title": "Unfallanzeige",
  ...       "name": "CK",
  ...       "age": "thirty"
  ... }
  ... '''
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++jsonapi/uaz',
  ... uaz_json_with_error, AUTHORIZATION=auth_header)

  >>> result = response.getBody()
  >>> print result
  [{"field": "age", "message": "Object is of wrong type."}]


An invariant uaz_xml file

  >>> uaz_json_with_invariant = '''
  ... {
  ...       "title": "Mein Unfall",
  ...       "name": "hans",
  ...       "age": 10
  ... }
  ... '''
  >>> response = http_call(wsgi_app(), 'PUT', 'http://localhost/++rest++jsonapi/uaz',
  ...  uaz_json_with_invariant, AUTHORIZATION=auth_header)
  >>> print response.getBody()
  [{"text": "Invariant: This combination of name and age is not valid"}]

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
