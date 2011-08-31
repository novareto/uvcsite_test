# -*- coding: utf-8 -*-
# Copyright (c) 2007-2011 NovaReto GmbH
# cklinger@novareto.de 

import grok
import tempfile

from zope.interface import Interface
from reportlab.pdfgen import canvas

class BasePDF(grok.View):
    grok.context(Interface)
    grok.baseclass()
    grok.name('pdf')
    grok.title('uvcsite.pdf')

    def file(self):
        return tempfile.TemporaryFile() 

    def filename(self):
        return grok.title.bind().get(self)

    def update(self):
        self.pdf = self.file()
        self.c = canvas.Canvas(self.pdf)
        self.genpdf()
        self.c.save()

    def genpdf(self):
        raise NotImplementedError

    def render(self):
        pdf = self.pdf
        pdf.seek(0)
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-length', pdf)
        RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' %self.filename)
        return pdf 
