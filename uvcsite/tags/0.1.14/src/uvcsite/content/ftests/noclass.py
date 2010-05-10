"""
  >>> class ContainerWithNoClass(ProductFolder):
  ...     contenttype('uvcsite.content.tests.container.MyContent')
  Traceback (most recent call last):
  ...
  GrokImportError: The 'contenttype' directive can only be called with a class.
"""
__grok__ = False

import grok
from uvcsite.content import ProductFolder, contenttype
