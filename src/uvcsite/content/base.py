import grok
from uvcsite.interfaces import IContentType


class Content(grok.Model):
    grok.implements(IContentType)
    grok.baseclass()

    @property
    def meta_type(self):
	return self.__class__.__name__
