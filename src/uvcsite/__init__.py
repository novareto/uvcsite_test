import grok
from uvcsite.content import (ProductFolder, IProductFolder, contenttype,
    IContent, Content, icon, schema, name)
from zope.i18nmessageid import MessageFactory
uvcsiteMF = MessageFactory('uvcsite')

from uvcsite.utils import TablePage, Page, ApplicationAwareView
