from zope.component import getUtility
from z3c.flashmessage.interfaces import IMessageSource
from uvcsite.content import IUVCApplication

class ApplicationAwareView(object):
    """A mixin allowing to access the application url"""

    def application_url(self, name=None):
        """Return the URL of the nearest Dolmen site.
        """
        obj = self.context
        while obj is not None:
            if IUVCApplication.providedBy(obj):
                return self.url(obj, name)
            obj = obj.__parent__
        print self.context
        raise ValueError("No application found.")


    def flash(self, message, type='message'):
       """Send a short message to the user.
       """
       source = getUtility(IMessageSource, name='session')
       source.send(message, type)

