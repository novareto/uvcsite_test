# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de

import grok
import uvcsite

from z3c.table.table import Table
from megrok.z3ctable import Column, table

grok.templatedir('templates')


class TableForm(uvcsite.Form, Table):
    grok.context(uvcsite.IUVCSite)
    grok.require('zope.View')
    cssClasses = {'table': 'table'}

    fields = uvcsite.Fields()

    def __init__(self, context, request):
        super(TableForm, self).__init__(context, request)
        Table.__init__(self, context, request)

    def update(self):
        super(TableForm, self).update()
        Table.update(self)

    @property
    def values(self):
        return [
            dict(id=1, name=u"Christian Klinger", alter="32"),
            dict(id=2, name=u"Lars Walther", alter="42"),
        ]

    def extractData(self):
        return self.request.form.get('form.field.cb_id'), ()

    @uvcsite.action(u'Speichern')
    def handle_save(self):
        data, errors = self.extractData()
        print data
        print errors


class CBColumn(Column):
    table(TableForm)
    grok.context(uvcsite.IUVCSite)
    header = "Name"
    cssClasses = {'td': 'right'}
    grok.name('cnc')

    def renderCell(self, item):
        selected = ""
        return u'<input type="checkbox" class="checkbox_widget" name="form.field.cb_id" value="%s" %s />' \
            %(item.get('id'), selected)


class NameColumn(Column):
    table(TableForm)
    grok.context(uvcsite.IUVCSite)
    header = "Name"
    cssClasses = {'td': 'right'}
    grok.name('tnc')

    def renderCell(self, item):
        return item['name']


class AlterColumn(Column):
    table(TableForm)
    grok.context(uvcsite.IUVCSite)
    header = "Alter"
    cssClasses = {'td': 'right'}
    grok.name('tac')

    def renderCell(self, item):
        return item['alter']
