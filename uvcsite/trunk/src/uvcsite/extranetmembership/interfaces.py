# -*- coding: utf-8 -*-

from uvcsite import uvcsiteMF as _
from zope.interface import Interface
from zope.schema import TextLine, Tuple, Choice, List


class IExtranetMember(Interface):

    mnr = TextLine(
             title = _(u"Mitgliedsnummer"),
             description = _(u"Mitgliedsnummer"),
             required = True)

    rollen = List(
             title=_(u"Berechtigung"),
             description=_(u"Berechtiung"),
             value_type=Choice(vocabulary="VocabularyBerechtigungen"),
             required = False)

    email = TextLine(
             title=_(u"Email"),
             description=_(u"Email"),
             required = True)

    passwort = TextLine(
              title = _(u"Passwort"),
              description = _(u"Passwort"),
              required = True)

    confirm = TextLine(
              title = _(u"Bestaetigung"),
              description = _(u"Bestaetigung"),
              required = True)

    def getBaseUser():
        """ Return the User Representation"""


class IUserManagement(Interface):

    def getUser(mnr):
        """ Return the specified User"""

    def getUserGroup(mnr):
        """ Return a group of a User from a company"""

    def addUser(**kw):
        """ Add a User to store """

    def updateUser(mnr, **kw):
        """ Update a specified user """

    def deleteUser(mnr):
        """ Delete a specified user """
