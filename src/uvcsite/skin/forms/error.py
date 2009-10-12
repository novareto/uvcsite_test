import os
import zope.component
import zope.interface
import uvcsite

from z3c.form import ptcompat, interfaces
from zope.pagetemplate.interfaces import IPageTemplate


class ErrorViewTemplateFactory(object):
    """Error view template factory."""

    template = None

    def __init__(self, filename, contentType='text/html'):
        self.template = ptcompat.ViewPageTemplateFile(
            filename, content_type=contentType)

    def __call__(self, errorView, request):
        return self.template

# Create the standard error view template
StandardErrorViewTemplate = ErrorViewTemplateFactory(
    os.path.join(os.path.dirname(uvcsite.content.__file__),
    'error.pt'), 'text/html')

zope.component.adapter(
    interfaces.IErrorViewSnippet, None)(StandardErrorViewTemplate)
zope.interface.implementer(IPageTemplate)(StandardErrorViewTemplate)
