# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

import grok
from zope.schema.vocabulary import SimpleVocabulary
from zope.app.schema.vocabulary import IVocabularyFactory


class VocabularyBerechtigungen(grok.GlobalUtility):
    """Vocabulary factory for workflow states.
    """
    grok.implements(IVocabularyFactory)
    grok.name('VocabularyBerechtigungen')

    def __call__(self, context):
        items = sorted((c, c) for c in context)
        return SimpleVocabulary.fromItems(items)
