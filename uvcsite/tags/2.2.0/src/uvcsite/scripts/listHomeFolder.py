# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

from sys import exit
from zope import component
from zope.app import homefolder
from pprint import pprint


def table_print(data, title_row):
    """data: list of dicts,
       title_row: e.g. [('name', 'Programming Language'), ('type', 'Language Type')]
    """
    max_widths = {}
    data_copy = [dict(title_row)] + list(data)
    for col in data_copy[0].keys():
        max_widths[col] = max([len(str(row[col])) for row in data_copy])
    cols_order = [tup[0] for tup in title_row]
       
    def custom_just(col, value):
        if type(value) == int:
            return str(value).rjust(max_widths[col])
        else:
            return value.ljust(max_widths[col])
   
    for row in data_copy:
        row_str = " | ".join([custom_just(col, row[col]) for col in cols_order])
        print "| %s |" % row_str
        if data_copy.index(row) == 0:
            underline = "-+-".join(['-' * max_widths[col] for col in cols_order])
            print '+-%s-+' % underline




APPNAME = "app"
USERNAME = "0101010001"

def listHomeFolder():
    uvcsite = root[APPNAME]
    component.hooks.setSite(uvcsite)
    hfm = component.getUtility(homefolder.interfaces.IHomeFolderManager)
    for id, productfolder in hfm.homeFolderBase.get(USERNAME).items():
        print
        print
        print 
        print "ProductFolder %s  ->> id %s" % (id.upper(), id)
        print
        rc = []
        for obj in productfolder.values():
            rc.append(dict(
                name=obj.__name__,
                titel=obj.title,
                ersteller=obj.principal.id,
                von=obj.modtime.strftime('%d.%m.%Y')
                ))
        table_print(rc, [('name', 'NameID'), ('titel', 'Titel'), ('ersteller', 'Ersteller'), ('von', 'Mod Datum')])
        print 
        print
        print "*"*80



if __name__ == "__main__":
    listHomeFolder()
    exit()
