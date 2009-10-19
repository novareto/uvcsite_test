# -*- coding: utf-8 -*-
# Copyright (c) 2007-2008 NovaReto GmbH
# cklinger@novareto.de

from zope.schema import TextLine
from zope.interface import implements
from zope.schema.interfaces import ITextLine
from zope.app.form.browser import MultiCheckBoxWidget
from zope.app.form.browser.widget import renderElement
from zope.app.form.browser.widget import SimpleInputWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.app.form.browser.textwidgets import PasswordWidget as BasePasswordWidget


class MultiCheckBoxVocabularyWidget(MultiCheckBoxWidget):
    """ """

    def __init__(self, field, request):
        """Initialize the widget."""
        super(MultiCheckBoxVocabularyWidget, self).__init__(field,
            field.value_type.vocabulary, request)


class LoginNameWidgetHidden(SimpleInputWidget):

    def __call__(self):
        context=self.context
        widget = ViewPageTemplateFile('templates/loginnamehidden.pt')
        return widget(self)

    def _getFormInput(self):
        value = super(LoginNameWidgetHidden, self)._getFormInput()
        return value


class CustomPasswordWidget(BasePasswordWidget):
    """Password Widget"""

    type = 'password'

    def __call__(self):
        value = self._getFormValue()
        displayMaxWidth = self.displayMaxWidth or 0
        if displayMaxWidth > 0:
            return renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 value=value,
                                 cssClass=self.cssClass,
                                 style=self.style,
                                 size=self.displayWidth,
                                 maxlength=displayMaxWidth,
                                 extra=self.extra)
        else:
            return renderElement(self.tag,
                                 type=self.type,
                                 name=self.name,
                                 id=self.name,
                                 cssClass=self.cssClass,
                                 style=self.style,
                                 size=self.displayWidth,
                                 value = value,
                                 extra=self.extra)

    def hidden(self):
        raise NotImplementedError(
            'Cannot get a hidden tag for a password field')

