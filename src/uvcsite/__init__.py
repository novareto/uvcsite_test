#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
uvcsiteMF = MessageFactory('uvcsite')


import grok
from uvcsite.content import (ProductFolder, IProductFolder, contenttype,
    IContent, Content, schema, name)

from megrok.layout import Page
from megrok.z3ctable import TablePage
from uvcsite.interfaces import *
from uvcsite.app import HelpPage
from dolmen.menu import menuentry, Entry, menu
from uvc.layout.menus import  Footer, SidebarMenu, GlobalMenu, category 
