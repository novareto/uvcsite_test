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
from uvcsite.utils.dataviews import BasePDF, BaseXML 
from uvc.layout.menus import  (Footer, GlobalMenu,
    PersonalMenu, PersonalPreferences, DocumentActionsMenu)
from uvc.layout.zeamform import (Form, AddForm,
    SubForm, GroupForm, Wizard, Step)
from uvc.layout.event import IAfterSaveEvent
from uvcsite.resources import Overlay, Tooltip, Mask

# Mobile
from uvcsite.mobile import MobilePage, MobileLayer, IMobileLayer


### ZEAM-FORM-API
from zeam.form.base import Fields, Action, Actions, action, DictDataManager
from zeam.form.base.markers import DISPLAY, INPUT, HIDDEN
from zeam.form.base.markers import SUCCESS, FAILURE, DEFAULT
from zeam.form.base.markers import NO_VALUE, NO_CHANGE, NOTHING_DONE
from zeam.form.ztk.actions import CancelAction
from zeam.form.base.errors import Error

### DOLMEN-FORMS-API
from dolmen.forms.base.models import ApplicationForm
from dolmen.forms.base.interfaces import IFieldUpdate
from dolmen.forms.base.utils import (
    set_fields_data, notify_changes, apply_data_event)

#from uvcsite.utils.mail import send_mail
from uvcsite.utils.olddata import Altdaten, PDF

### LOGGING
import logging
logger = logging.getLogger('uvcsite')

def log(message, summary='', severity=logging.INFO):
    logger.log(severity, '%s %s', summary, message)
