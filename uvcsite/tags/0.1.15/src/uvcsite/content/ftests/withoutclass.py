"""
  >>> import grok.testing
  >>> grok.testing.grok(__name__)
  Traceback (most recent call last):
  ...
  GrokError: <class 'uvcsite.content.ftests.withoutclass.PF'> must specify which contenttype should go into this ProductFolder. Please use thedirecitve 'contenttype' for it.
"""
__grok__ = False

import grok
from uvcsite.content import ProductFolder, contenttype


class PF(ProductFolder):
    pass
