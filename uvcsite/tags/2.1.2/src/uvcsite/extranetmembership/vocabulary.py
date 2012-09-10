# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grokcore.component as grok
from uvcsite.content.productregistration import getProductRegistrations
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def vocabulary(terms):
    """ """
    return SimpleVocabulary(
        [SimpleTerm(value, token, title) for value, token, title in terms])


@grok.provider(IContextSourceBinder)
def vocab_berechtigungen(context):
    rc = []
    for d in getProductRegistrations():
        id, reg = d
        if reg.asRole == True:
            rc.append(SimpleTerm(reg.folderURI, reg.folderURI, reg.linkname))
    return SimpleVocabulary(rc)
