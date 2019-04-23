#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: First Test
# Generated: Tue Apr 23 13:57:30 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print ("Warning: failed to XInitThreads()")

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import sys
import time
from gnuradio import qtgui


class first_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "First Test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("First Test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "first_test")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2000000
        self.freq = freq = 2420000000

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0_1_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.5", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_1_0.set_time_source('external', 0)
        self.uhd_usrp_source_0_1_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_1_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0_1_0.set_gain(0, 0)
        self.uhd_usrp_source_0_1_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0_1_0.set_bandwidth(40000000, 0)
        self.uhd_usrp_source_0_1 = uhd.usrp_source(
        	",".join(("addr=192.168.10.4", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_1.set_time_source('external', 0)
        self.uhd_usrp_source_0_1.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_1.set_center_freq(freq, 0)
        self.uhd_usrp_source_0_1.set_gain(0, 0)
        self.uhd_usrp_source_0_1.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0_1.set_bandwidth(40000000, 0)
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.3", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_0.set_time_source('external', 0)
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0_0.set_gain(0, 0)
        self.uhd_usrp_source_0_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0_0.set_bandwidth(40000000, 0)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.3", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_source_0.set_bandwidth(40000000, 0)
        self.blocks_udp_sink_1 = blocks.udp_sink(gr.sizeof_gr_complex*1, '192.168.10.1', 12346, 1472, True)
        self.blocks_udp_sink_0_0_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '192.168.10.1', 12348, 1472, True)
        self.blocks_udp_sink_0_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '192.168.10.1', 12347, 1472, True)
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_gr_complex*1, '192.168.10.1', 12345, 1472, True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_udp_sink_0, 0))
        self.connect((self.uhd_usrp_source_0_0, 0), (self.blocks_udp_sink_1, 0))
        self.connect((self.uhd_usrp_source_0_1, 0), (self.blocks_udp_sink_0_0, 0))
        self.connect((self.uhd_usrp_source_0_1_0, 0), (self.blocks_udp_sink_0_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "first_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0_1_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_1.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0_1_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0_1_0.set_center_freq(self.freq, 1)
        self.uhd_usrp_source_0_1.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0_1.set_center_freq(self.freq, 1)
        self.uhd_usrp_source_0_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0_0.set_center_freq(self.freq, 1)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 1)


def main(top_block_cls=first_test, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
