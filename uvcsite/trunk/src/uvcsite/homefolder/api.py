import grok
from lxml import etree
from StringIO import StringIO
from uvcsite.app import RestLayer
from uvcsite.interfaces import IMyHomeFolder
from zope.component import createObject, getUtility
from zope.component.interfaces import IFactory
from zope.interface import Invalid
from zope.schema import getFields, ValidationError



class ARest(grok.REST):
    grok.layer(RestLayer)
    grok.context(IMyHomeFolder)

    def GET(self):
        eoot = etree.Element('container')
        for id, obj in self.context.items():
            object = etree.SubElement(root, obj.meta_type)
            id = etree.SubElement(object, 'id').text = id
            name = etree.SubElement(object, 'name').text = obj.name
            vorname = etree.SubElement(object, 'vorname').text=obj.vorname
        return etree.tostring(root, pretty_print=True)

    def POST(self):
        return "POST"

    def PUT(self):
        root = etree.Element('xml')
        tree = etree.parse(StringIO(self.body))
        objects = tree.xpath('/object')
        # get the Factory for the Object
        for object in objects:
            ok = True 
            mt = object.attrib
            if mt:
                meta_type = "uvc.%s"  %mt.get('meta_type')
                factory = getUtility(IFactory, name=meta_type)
            # Get the first Interface           
            interface = [x for x in factory.getInterfaces()][0]
            # Get the Object
            type = factory()
            for name, field in getFields(interface).items():
                value = object.find(name)
                if value is not None:
                    #setattr(type, name, unicode(value.text))
                    try:
                        setattr(type, name, unicode(value.text))
                    except ValidationError, e:
                        error = etree.SubElement(root, 'error')
                        error.set('field', name)
                        message = etree.SubElement(error, 'message')
                        message.set(value.text, e.doc())
                        ok = False
            # Check for Global Invariants
            try:
                interface.validateInvariants(type)
            except Invalid, e:
                error = etree.SubElement(root, 'error')
                error.text = str(e)
                ok = False
            #import pdb; pdb.set_trace()
            if ok:
                id = "person-%s" %(str(len(self.context)))
                self.context[id]= type
                success = etree.SubElement(root, 'success')
                success.text = type.name
                success.set('id', id)
        return etree.tostring(root, pretty_print=True) 

    def DELETE(self):
        return "DELETE"
