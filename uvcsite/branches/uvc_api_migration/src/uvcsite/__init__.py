#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
uvcsiteMF = MessageFactory('uvcsite')


### LOGGING
import logging
logger = logging.getLogger('uvcsite')

def log(message, summary='', severity=logging.INFO):
    logger.log(severity, '%s %s', summary, message)
