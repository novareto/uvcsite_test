# -*- coding: utf-8 -*-

from zeam.form.base import NO_VALUE
from zeam.form.ztk import customize
from zeam.form.ztk.widgets.choice import RadioFieldWidget
from zeam.form.ztk.widgets.collection import MultiChoiceFieldWidget
from zeam.form.ztk.widgets.date import DateWidgetExtractor
from zope.schema.interfaces import IDate
from zope.i18n.format import DateTimeParseError


class UvcRadioFieldWidget(RadioFieldWidget):
    """ Simple Override for removing <br> between choices
    """
    pass


class UvcMultiChoiceFieldWidget(MultiChoiceFieldWidget):
    """ Simple Override for removing <br> between choices
    """


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


@customize(origin=IDate)
def customize_size(field):
    field.valueLength = 'medium'
