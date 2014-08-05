# -*- coding: utf-8 -*-

import uvclight
from dolmen.message import receive
from uvc.design.canvas.managers import IAboveContent


class FlashMessages(uvclight.Viewlet):
    uvclight.viewletmanager(IAboveContent)

    def render(self):
        messages = [msg.message for msg in receive()]
        return '<br />'.join(messages)
