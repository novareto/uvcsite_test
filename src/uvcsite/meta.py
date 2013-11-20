# -*- coding: utf-8 -*-

import martian
from .app import Uvcsite
from grokcore.site.interfaces import IApplication
from grokcore.component import provideUtility


class UVCSiteGrokker(martian.ClassGrokker):
    """Grokker for Grok application classes."""
    martian.component(Uvcsite)
    martian.priority(500)

    def grok(self, name, factory, module_info, config, **kw):
        provides = IApplication
        name = '%s.%s' % (module_info.dotted_name, name)
        config.action(
            discriminator=('utility', provides, name),
            callable=provideUtility,
            args=(factory, provides, name),
            )
        return True
