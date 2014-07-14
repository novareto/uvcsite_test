# -*- coding: utf-8 -*-

from dolmen.forms.ztk.widgets.choice import RadioFieldWidget
from dolmen.forms.ztk.widgets.collection import MultiChoiceFieldWidget
from dolmen.forms.ztk.widgets.date import DateWidgetExtractor
from dolmen.forms.base import NO_VALUE
#from dolmen.forms.ztk import customize
from zope.i18n.format import DateTimeParseError
from zope.schema.interfaces import IDate


class UVCDateWidgetExtractor(DateWidgetExtractor):

    def extract(self):
        value, error = super(DateWidgetExtractor, self).extract()
        if value is not NO_VALUE:
            if not len(value):
                return NO_VALUE, None
            formatter = self.component.getFormatter(self.form)
            try:
                value = formatter.parse(value)
            except (ValueError, DateTimeParseError), error:
                return None, u"Bitte überprüfen Sie das Datumsformat."
        return value, error

    
## @customize(origin=IDate)
## def customize_size(field):
##     field.valueLength = 'medium'


class UvcRadioFieldWidget(RadioFieldWidget):
    """ Simple Override for removing <br> between choices
    """
    pass


class UvcMultiChoiceFieldWidget(MultiChoiceFieldWidget):
    """ Simple Override for removing <br> between choices
    """
