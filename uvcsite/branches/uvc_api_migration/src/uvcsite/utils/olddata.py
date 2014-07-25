# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import base64
import uvclight
import time
import datetime
import uvcsite
import xmlrpclib
from megrok.z3ctable import table
from uvcsite.content import IProductFolder


class Altdaten(uvclight.TablePage):
    """ """
    uvclight.baseclass()
    template = uvclight.get_template('altdaten.cpt', __file__)
    uvclight.title(u'Alte Dokumente')

    cssClasses = {'table': 'tablesorter'}
    title = u"Alte Dokumente"
    description = u"Hier finden Sie die vor dem 30.Mai.2011 erstellten Unfallanzeigen."

    object_type = ""

    @property
    def values(self):
        raise NotImplementedError


class Title(uvclight.Column):
    """ """
    uvclight.name('title')
    table(Altdaten)
    uvclight.context(IProductFolder)
    header = u"Titel"
    weight = 10

    def renderCell(self, item):
        url = "%s/@@pdf?id=%s" % (self.table.url(), item['id'])
        link = '<a href="%s"> %s </a>' % (url, item['title'])
        return link


class Autor(uvclight.Column):
    """ """
    uvclight.name('autor')
    table(Altdaten)
    uvclight.context(IProductFolder)
    header = u"Erstellt von"
    weight = 20

    def renderCell(self, item):
        return item['Creator']


class Status(uvclight.Column):
    """ """
    uvclight.name('status')
    table(Altdaten)
    uvclight.context(IProductFolder)
    header = u"Status"
    weight = 30

    def renderCell(self, item):
        return item['review_state']


class Datum(uvclight.Column):
    """ """
    uvclight.name('datum')
    table(Altdaten)
    uvclight.context(IProductFolder)
    header = u"Datum"
    weight = 40

    def renderCell(self, item):
        datumString = item['ModificationDate']
        datumFmt = "%Y-%m-%d %H:%M:%S"
        datum = datetime.datetime.fromtimestamp(time.mktime(time.strptime(datumString, datumFmt)))
        datum = datum.strftime("%d.%m.%Y %H:%M:%S")
        return datum


class PDF(uvclight.View):
    uvclight.view(Altdaten)
    uvclight.context(Altdaten)
    uvclight.baseclass()

    def url(self):
        raise NotImplementedError

    def render(self):
        oid = self.request.get('id')
        principal = self.request.principal.id
        URL = self.url()
        server = xmlrpclib.ServerProxy(URL)
        content = server.asRemotePdf(oid, principal)
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-disposition', 'attachment; filename=unfallanzeige.pdf')
        return base64.decodestring(content)
