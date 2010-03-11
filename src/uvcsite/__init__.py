#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
uvcsiteMF = MessageFactory('uvcsite')


import grok
from uvcsite.content import (ProductFolder, IProductFolder, contenttype,
    IContent, Content, schema, name)

from uvcsite.viewlets.utils import MenuItem
from megrok.layout import Page
from megrok.z3ctable import TablePage
from uvcsite.interfaces import *
