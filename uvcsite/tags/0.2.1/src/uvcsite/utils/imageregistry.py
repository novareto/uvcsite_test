import grok

from megrok import icon
from zope.interface import Interface
from zope.component import getUtility

class IconRegistryView(grok.MultiAdapter):
    grok.adapts(Interface, grok.IBrowserRequest)
    grok.name('image_req')
    grok.provides(Interface)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.registry = getUtility(icon.IIconRegistry, name="uvc-icons")

    def get_icon_url(self, image=None):
        if self.registry is not None:
            return icon.get_icon_url(self.registry, self.request, image)
        return "Something!"
