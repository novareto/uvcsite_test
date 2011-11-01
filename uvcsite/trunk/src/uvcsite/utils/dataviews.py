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

    def getFile(self, fn):
        if fn:
            return open(fn, 'w+b')
        return tempfile.TemporaryFile() 

    @property
    def filename(self):
        return grok.title.bind().get(self)

    def update(self, filename=None):
        self.pdf_file = self.getFile(filename)
        self.c = canvas.Canvas(self.pdf_file)
        self.genpdf()
        self.c.save()

    def create(self, fn):
        self.update(fn)
        self.pdf_file.close()

    def genpdf(self):
        raise NotImplementedError

    def render(self):
        pdf = self.pdf_file
        pdf.seek(0)
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'application/pdf')
        RESPONSE.setHeader('content-length', pdf)
        RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' %self.filename)
        return pdf 


class BaseXML(BasePDF):
    grok.name('xml')
    grok.title('uvcsite.xml')

    def update(self, filename=None):
        self.xml_file = self.file(filename)
        self.genxml()

    def genxml(self):
        raise NotImplementedError

    def render(self):
        xml = self.xml_file
        xml.seek(0)
        RESPONSE = self.request.response
        RESPONSE.setHeader('content-type', 'text/xml')
        RESPONSE.setHeader('content-length', xml)
        RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' %self.filename)
        return xml 
