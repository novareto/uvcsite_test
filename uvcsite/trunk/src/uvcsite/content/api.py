#!/usr/bin/python
# -*- coding: utf-8 -*-

import grok


from lxml import etree
from dolmen.content import IContent
from uvcsite.content import IProductFolder
from zope.component import getMultiAdapter
from zope.interface import Invalid, Interface
from zope.pagetemplate.interfaces import IPageTemplate
from z3c.schema2xml import serialize_to_tree, deserialize


class RestLayer(grok.IRESTLayer):
    """ Layer for Rest Access"""
    grok.restskin('api')


class ProductFolderRest(grok.REST):
    grok.layer(RestLayer)
    grok.context(IProductFolder)
    grok.require('zope.View')

    def GET(self):
        context = self.context
        container = etree.Element('container', id=context.__name__)
        for id, obj in self.context.items():
            schema = obj.schema[0]
            element = etree.SubElement(container, obj.meta_type, id=id)
            serialize_to_tree(element, schema, obj)
        return etree.tostring(container, encoding='UTF-8', pretty_print=True)

    def POST(self):
        return "POST"

    def PUT(self):
        errors = []
        content = self.context.getContentType()()
        interface = content.schema[0]
        serializer = ISerializer(content)
        serializer.work(self.body, interface, errors)

        if not errors:
            self.context.add(content)
            result = etree.Element(
                'success', 
                name=content.meta_type,
                id=content.__name__
                )
        else:
            result = etree.Element('failure')
            result.extend(errors)
        return etree.tostring(result, encoding='UTF-8', pretty_print=True)


class ISerializer(Interface):
    """ Base Serialzer for IContent Objects
    """

    def work(payload, interface, errors):
        """ Worker which populates self.context
            with the contents of the payload and
            with the help of interface
        """


class DefaultSerializer(grok.Adapter):
    """ Default Serializer for IContent
    """

    grok.context(IContent)
    grok.implements(ISerializer)

    def work(self, payload, interface, errors):
        try:
            deserialize(payload, interface, self.context)
        except Exception, e: # Here should be a DeserializeError
            for field, (exception, element) in e.field_errors.items():
                error = etree.Element('error', field=field.__name__,
                    message=exception.__doc__)
                error.append(element)
                errors.append(error)
        try:
            interface.validateInvariants(self.context)
        except Invalid, e:
            errors.append(etree.Element('error', text="Invariant: %s" % e))
