# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
from zope.app.homefolder.interfaces import IHomeFolder
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


def vocabulary(terms):
    """ """
    return SimpleVocabulary([SimpleTerm(value, token, title) for value, token, title in terms])


class VocabularyBerechtigungen(grok.GlobalUtility):
    """Vocabulary factory for workflow states.
    """
    grok.implements(IVocabularyFactory)
    grok.name('VocabularyBerechtigungen')

    def __call__(self, context):
        items = sorted((c, c, c) for c in context.keys())
        return vocabulary(items)
