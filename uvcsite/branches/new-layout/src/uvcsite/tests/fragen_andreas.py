# -*- coding: utf-8 -*-
# Copyright (c) 2007-2010 NovaReto GmbH
# cklinger@novareto.de 

import grok
import uvcsite


class AuskunftEntry(uvcsite.MenuItem):
    """ Ein Eintrag im Globalen Menu ohne Dropdown
        Achtung in der Zeile layout.menus.category
        dropdown=False
    """
    grok.title('Auskunft')
    grok.viewletmanager(uvcsite.IGlobalMenu)
    grok.order(20000)

    action = "http://www.google.de"
