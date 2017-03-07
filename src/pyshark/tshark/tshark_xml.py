"""
This module contains functions to turn TShark XML parts into Packet objects.
"""
import lxml.objectify
from pyshark.packet.packet import Packet

def psml_structure_from_xml(psml_structure):
    if not isinstance(psml_structure, lxml.objectify.ObjectifiedElement):
        psml_structure = lxml.objectify.fromstring(psml_structure)
    return psml_structure.findall('section')

def packet_from_xml_packet(xml_pkt):
    """
    Gets a TShark XML packet object or string, and returns a pyshark Packet objec.t

    :param xml_pkt: str or xml object.
    :return: Packet object.
    """
    if not isinstance(xml_pkt, lxml.objectify.ObjectifiedElement):
        parser = lxml.objectify.makeparser(huge_tree=True)
        xml_pkt = lxml.objectify.fromstring(xml_pkt, parser)
    return _packet_from_pdml_packet(xml_pkt)

def _packet_from_pdml_packet(pdml_packet):
    """
    Transforms XML object to Packet instance

    :param pdml_packet: lxml.objectify.ObjectifiedElement
    :return: Packet instance
    """
    return Packet(pdml_packet = pdml_packet)

def packets_from_xml(xml_data):
    """
    Returns a list of Packet objects from a TShark XML.

    :param xml_data: str containing the XML.
    """
    pdml = lxml.objectify.fromstring(xml_data)
    packets = []

    for xml_pkt in pdml.getchildren():
        packets += [packet_from_xml_packet(xml_pkt)]
    return packets