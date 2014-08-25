#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
uvcsiteMF = MessageFactory('uvcsite')

import grok
from uvcsite.content import (ProductFolder, IProductFolder, contenttype,
    IContent, Content, schema, name, productfolder)
from uvcsite.interfaces import *
from uvcsite.utils.help import HelpPage
from uvc.layout.slots.menus import  (Footer, GlobalMenu,
    PersonalMenu, PersonalPreferences, DocumentActionsMenu)
from uvcsite.utils.dataviews import BasePDF, BaseXML, BaseDataView, WatermarkPDF
from uvc.layout.forms import AddForm, SubForm, GroupForm, Wizard, Step
from megrok.z3ctable import TablePage
from uvc.layout.forms import (Form, AddForm, SubForm, GroupForm, Wizard, Step)
from uvc.layout import *
#from uvc.api import *

from uvc.layout.forms.event import IAfterSaveEvent

# Mobile
# from uvcsite.mobile import BaseMobilePage, MobilePage, MobileLayer, IMobileLayer

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
from dolmen.forms.base.utils import notify_changes, apply_data_event
from uvcsite.utils.form import set_fields_data

#from uvcsite.utils.mail import send_mail
from uvcsite.utils.olddata import Altdaten, PDF
from uvcsite.utils.shorties import fmtDate, fmtFloat, fmtZahl, getPrincipal, getRequest, fmtDateTime, getHomeFolderUrl, getHomeFolder
from uvcsite.auth.interfaces import IMasterUser
from uvcsite.content.productregistration import (ProductRegistration,
    getProductRegistrations, getAllProductRegistrations, ProductMenuItem)

### LOGGING
import logging
logger = logging.getLogger('uvcsite')

def log(message, summary='', severity=logging.INFO):
    logger.log(severity, '%s %s', summary, message)
