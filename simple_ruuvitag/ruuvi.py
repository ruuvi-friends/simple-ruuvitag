import os
import datetime
import logging

from simple_ruuvitag.data_formats import DataFormats
from simple_ruuvitag.decoder import get_decoder

from simple_ruuvitag.adaptors.dummy import DummyBle
from simple_ruuvitag.adaptors.bleson import BlesonClient

log = logging.getLogger(__name__)

class RuuviTagClient(object):
    """
    RuuviTag communication functionality
    """

    def __init__(self, adapter='bleson'):

        if os.environ.get('CI') == 'True':
            log.warn("Adapter override to Dummy due to CI env variable")
            self.ble = DummyBle()

        if adapter == 'dummy':
            self.ble = DummyBle()

        elif adapter == 'bleson':
            self.ble = BlesonClient()
        else:
            raise RuntimeError("Unsupported adapter %s" % adapter)

        self.mac_blacklist = []
        self.callback = print
        self.mac_addresses = None
        self.latest_data = {}

    def listen(self, callback=log.info, mac_addresses=None):
        if mac_addresses:
            if isinstance(mac_addresses, list):
                self.mac_addresses = [x.upper() for x in mac_addresses]
            else:
                self.mac_addresses = mac_addresses.upper()

        self.callback = callback
        self.ble.start(self.convert_data_and_callback)

    def rescan(self):
        self.ble.rescan()

    def stop(self):
        self.ble.stop() 

    def get_current_datas(self, consume=False):
        """
        Get current data gets the current state of the known tags.
        If consume=True it will delete the current data so that old 
        readings don't get interpreted as current readings.
        """
        return_data = self.latest_data.copy()
        if consume:
            self.latest_data = {}

        return return_data

    def convert_data_and_callback(self, data):
        """
        This callback updates the current data, and calls the callback
        """
        log.debug('Callback with data: %s', data)

        # {
        #     "address": "MAC ADDRESS IN UPPERCASE"
        #     "raw_data":  
        #     "rssi": 
        #     "tx_power"
        #     "name": st
        # }

        mac_address = data["address"]
        raw_data = data["raw_data"]

        if mac_address in self.mac_blacklist:
            log.debug("Skipping blacklisted mac %s" % mac_address)
            return

        if self.mac_addresses and mac_address not in self.mac_addresses:
            log.debug("Skipping non selected mac %s" % mac_address)
            return

        (data_format, data) = DataFormats.convert_data(raw_data)

        if data is not None:
            state = get_decoder(data_format).decode_data(data)
            if state is not None:
                self.latest_data[mac_address] = state
                self.latest_data[mac_address]['_updated_at'] = datetime.datetime.now()
                self.callback(mac_address, state)
            else:
                log.error('Decoded data is null. MAC: %s - Raw: %s', mac_address, raw_data)
        else:
            self.mac_blacklist.append(mac_address)