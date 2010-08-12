#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
uvcsiteMF = MessageFactory('uvcsite')

# MenuStuff
from uvc.layout.menus import SubMenu as Category
from megrok.navigation import sitemenuitem as menu
from megrok.navigation import parentmenu as topmenu
from megrok.navigation import menuitem as sectionmenu 


import grok
from uvcsite.content import (ProductFolder, IProductFolder, contenttype,
    IContent, Content, schema, name)

from megrok.layout import Page
from megrok.z3ctable import TablePage
from uvcsite.interfaces import *
from uvcsite.utils.help import HelpPage
from uvc.layout.menus import  (Footer, GlobalMenu, 
         PersonalMenu, PersonalPreferences, DocumentActionsMenu)
from uvcsite.utils.zeamform import Form, AddForm, SubForm, GroupForm, Wizard, Step


from uvcsite.tests import ipython
