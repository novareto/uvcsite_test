import grok

from uvcsample.unfall import IUnfall
from uvcsite.helpsystem.portlet import HelpPortlet

class UAZHilfe(HelpPortlet):
    grok.context(IUnfall)

    urls = [{'href': 'hilfe', 'name': 'hilfe'}]
