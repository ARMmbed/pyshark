from pyshark.capture.capture import Capture
from pyshark.tshark.tshark import get_tshark_interfaces
import sys

# Define basestring as str if we're in python3.
if sys.version_info >= (3, 0):
    basestring = str

class LiveCapture(Capture):
    """
    Represents a live capture on a network interface.
    """

    def __init__(self, interface=None, bpf_filter=None, display_filter=None, only_summaries=False, output_file=None, decode_as=None, tshark_path=None, override_prefs=None, capture_filter=None, tshark_arguments=None):
        """
        Creates a new live capturer on a given interface. Does not start the actual capture itself.

        :param interface: Name of the interface to sniff on or a list of names (str). If not given, runs on all interfaces.
        :param bpf_filter: BPF filter to use on packets.
        :param display_filter: Display (wireshark) filter to use.
        :param only_summaries: Only produce packet summaries, much faster but includes very little information
        :param output_file: Additionally save live captured packets to this file.
        :param decode_as: A dictionary of {decode_criterion_string: decode_as_protocol} that are used to tell tshark
        to decode protocols in situations it wouldn't usually, for instance {'tcp.port==8888': 'http'} would make
        it attempt to decode any port 8888 traffic as HTTP. See tshark documentation for details.
        :param tshark_path: Path of the tshark binary
        :param override_prefs: A dictionary of tshark preferences to override, {PREFERENCE_NAME: PREFERENCE_VALUE, ...}.
        :param capture_filter: Capture (wireshark) filter to use.
        """
        super(LiveCapture, self).__init__(display_filter=display_filter, only_summaries=only_summaries,
                                          output_file=output_file, decode_as=decode_as, tshark_path=tshark_path,
                                          override_prefs=override_prefs, capture_filter=capture_filter)
        self.bpf_filter = bpf_filter
        
        if interface is None:
            self.interfaces = get_tshark_interfaces(tshark_path)
        elif isinstance(interface, basestring):
            self.interfaces = [interface]
        else:
            self.interfaces = interface

    def get_parameters(self, packet_count=None):
        """
        Returns the special tshark parameters to be used according to the configuration of this class.
        """
        params = super(LiveCapture, self).get_parameters(packet_count=packet_count)
        if self.bpf_filter:
            params += ['-f', self.bpf_filter]
        for interface in self.interfaces:
            params += ['-i', interface]
        return params

    # Backwards compatibility
    sniff = Capture.load_packets

    def sniff_continuously(self, packet_count=None):
        """
        Captures from the set interface, returning a generator which returns packets continuously.

        Can be used as follows:
        for packet in capture.sniff_continuously();
            print 'Woo, another packet:', packet

        Note: you can also call capture.apply_on_packets(packet_callback) which should have a slight performance boost.

        :param packet_count: an amount of packets to capture, then stop.
        """
        # Retained for backwards compatibility and to add documentation.
        return self._packets_from_tshark_sync(packet_count=packet_count)
