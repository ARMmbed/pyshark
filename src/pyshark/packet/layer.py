import os
import binascii
import py

class Field(object):
    """
    Holds all data about a field of a layer.
    """
    # Note: We use this object with slots and not just a dict because
    # it's much more memory-efficient (cuts about a third of the memory).
    __slots__ = ['name', 'field', 'proto', 'showname', 'raw_value', 'show', 'hide', 'pos', 'size', 'unmaskedvalue']

    def __init__(self, name=None, field=None, proto=None, showname=None, value=None, show=None, hide=None, pos=None, size=None, unmaskedvalue=None):
        self.name = name
        self.showname = showname
        self.raw_value = value
        self.show = show
        self.pos = pos
        self.size = size
        self.unmaskedvalue = unmaskedvalue
        self.field = field
        self.proto = proto

        if hide and hide == 'yes':
            self.hide = True
        else:
            self.hide = False

class Layer():
    """
    An object representing a Packet layer.
    """

    def __init__(self, xml_obj=None):
        # We copy over all the fields from the XML object
        # Note: we don't read lazily from the XML because the lxml objects are very memory-inefficient
        # so we'd rather not save them.
        self.fields = self.objectify(xml_obj)
        self.layer_name = self.fields.name.lower()
        self.proto = self.fields.proto
        self.field = self.fields.field

    def objectify(self, obj):
        """
        Recursing method for copying nested fields from XML object
        """
        attributes = dict(obj.attrib)

        fields = [self.objectify(field) for field in obj.findall('./field')]
        subfield = fields or None

        protos = [self.objectify(field) for field in obj.findall('./proto')]
        subproto = protos or None

        fld_obj = Field(field=subfield, proto=subproto, **attributes)
        return fld_obj

    def pretty_print(self):
        # TODO: print prettily
        return
        tw = py.io.TerminalWriter()
        tw.write("rutabaga" + os.linesep, yellow=True, bold=True)
        tw.write(field_name + ':', green=True, bold=True)