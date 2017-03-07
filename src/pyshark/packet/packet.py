import datetime
import os
from pyshark.packet.layer import Layer

class Packet():
    """
    A packet object which contains layers.
    Layers can be accessed via index or name.
    """

    def __init__(self, pdml_packet=None):
        """
        Creates a Packet object with the given layers and info.

        :param layers: A list of Layer objects.
        :param frame_info: Layer object for the entire packet frame (information like frame length, packet number, etc.
        :param length: Length of the actual packet.
        :param captured_length: The length of the packet that was actually captured (could be less then length)
        :param sniff_time: The time the packet was captured (timestamp)
        :param interface_captured: The interface the packet was captured in.
        """

        # TODO: retrieve metadata

        # frame_info=None, number=None, length=None, captured_length=None, sniff_time=None, interface_captured=None
        
        # TODO: simple search function for layer, then metadata retrieval
        
        if pdml_packet is not None:
            self.layers = [Layer(proto) for proto in pdml_packet.proto]
            #self.frame_info = frame_info
            #self.number = number
            #self.interface_captured = interface_captured
            #self.captured_length = captured_length
            #self.length = length
            #self.sniff_timestamp = sniff_time
        else:
            self.layers = []
            
            #geninfo = self.findLayer("geninfo")
            frame = self.findLayer("frame")

            self.frame_info = ''
            self.number = frame.findField("frame.number")
            self.interface_captured = ''
            self.captured_length = frame.findField("frame.cap_len")
            self.length = length = frame.findField("frame.len")
            self.sniff_timestamp = frame.findField("frame.time_relative")
            self.epoch_time = frame.findField("frame.time_epoch")

    def __getitem__(self, item):
        """
        Gets a layer according to its index or its name

        :param item: layer index or name
        :return: Layer object.
        """
        if isinstance(item, int):
            return self.layers[item]
        if item == 'packet':
            return self
        else:
            for layer in self.layers:
                if layer.layer_name == item.lower():
                    return layer

        raise KeyError('Layer does not exist in packet')

    def __getattr__(self, item):
        """
        Allows layers to be retrieved via get attr. For instance: pkt.ip
        """
        for layer in self.layers:
            if layer.layer_name == item:
                return layer
        raise AttributeError()

    def pretty_print(self):
        for layer in self.layers:
            layer.pretty_print()

    @property
    def highest_layer(self):
        return self.layers[-1].layer_name

    @property
    def layer_names(self):
        """
        Returns all layer names
        """
        return [layer.layer_name for layer in self.layers]

    def findLayer(self, name):
        """
        Returns layer in packet if exists, None otherwise
        """
        for layer in self.layers:
            if layer.layer_name == name:
                return layer
        return None
