"""
:doctest:
:layer: uvcsite.tests.FunctionalLayer

The ProductFolder should have a class in every case.
----------------------------------------------------

  >>> from uvcsite.content import ProductFolder, contenttype
  >>> class ContainerWithNoClass(ProductFolder):
  ...     contenttype('uvcsite.content.tests.container.MyContent')
  Traceback (most recent call last):
  ...
  GrokImportError: The 'contenttype' directive can only be called with a class.

"""
