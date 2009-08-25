# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

from zope.schema import TextLine
from zope.interface import implements
from zope.schema.interfaces import ITextLine
from zope.app.form.browser import MultiCheckBoxWidget
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class MultiCheckBoxVocabularyWidget(MultiCheckBoxWidget):
    """ """

    def __init__(self, field, request):
        """Initialize the widget."""
        super(MultiCheckBoxVocabularyWidget, self).__init__(field,
            field.value_type.vocabulary, request)


class ILoginNameFieldHidden(ITextLine):
    """ Login Field in form of xxx@mnr"""


class LoginNameFieldHidden(TextLine):
    implements(ILoginNameFieldHidden)

    def __init__(self, **kw):
        super(LoginNameFieldHidden, self).__init__(**kw)


class LoginNameWidgetHidden(SimpleInputWidget):

    def __call__(self):
        context=self.context
        widget = ViewPageTemplateFile('templates/loginnamehidden.pt')
        return widget(self)

    def _getFormInput(self):
        value = super(LoginNameWidgetHidden, self)._getFormInput()
        return value
