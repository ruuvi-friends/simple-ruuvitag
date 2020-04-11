import os
from datetime import datetime
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
    def __init__(self, callback=log.info, mac_addresses=None,
                 bt_device=None, adapter='bleson'):

        if os.environ.get('CI') == 'True':
            log.info("Adapter override to Dummy due to CI env variable")
            self.ble_adaptor = DummyBle

        if adapter == 'dummy':
            self.ble_adaptor = DummyBle

        elif adapter == 'bleson':
            self.ble_adaptor = BlesonClient
        else:
            raise RuntimeError("Unsupported adapter %s" % adapter)

        # Setup defaults
        self.mac_blacklist = []
        self.callback = print
        self.mac_addresses = None

        self.latest_data = {}
        if mac_addresses:
            if isinstance(mac_addresses, list):
                self.mac_addresses = [x.upper() for x in mac_addresses]
            else:
                self.mac_addresses = mac_addresses.upper()

        self.callback = callback
        self.ble = self.ble_adaptor(
            self.convert_data_and_callback, bt_device=bt_device
        )

    def resume(self):
        self.ble.start()

    def start(self):
        self.ble.start()

    def rescan(self):
        self.ble.stop()
        self.ble.start()

    def stop(self):
        self.ble.stop()

    def pause(self):
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
        #     "raw_data": xxxx
        # }

        raw_data = data["raw_data"]
        mac_address = data["address"]

        if not raw_data:
            return

        if mac_address:
            # Standardise mac address to upper case
            mac_address = mac_address.upper()
            if mac_address in self.mac_blacklist:
                log.debug("Skipping blacklisted mac %s", mac_address)
                return
            if self.mac_addresses and mac_address not in self.mac_addresses:
                log.debug("Skipping non listed mac address %s", mac_address)
                return

        (data_format, converted_raw_data) = DataFormats.convert_data(raw_data)

        if not converted_raw_data:
            if mac_address:
                self.mac_blacklist.append(mac_address)
            return

        decoded_data = get_decoder(data_format).decode_data(converted_raw_data)

        if not decoded_data:
            if mac_address:
                self.mac_blacklist.append(mac_address)
            return

        if not mac_address:
            log.debug("Attempting to fallback to payload mac addr.")
            # Some adaptors and OS don't provide the mac addresses 
            # (*cough* shitty apple *cough*), so we need to try and 
            # get it from Ruuvi payload. However that is only possible 
            # in V5 data format. All others will be discarded :(

            mac_address = decoded_data.get('mac', None)

            if not mac_address:
                log.warning(
                    "DATA TYPE IS NOT SUPPORTED BY MAC OS. "
                    "UPDATE YOUR TAG AND SWITCH MODE"
                )
                return
            else:
                # format it nicely
                mac_address = mac_address.upper()
                mac_address = ':'.join(mac_address[i:i+2] for i in range(0,12,2))

        self.latest_data[mac_address] = decoded_data
        self.latest_data[mac_address]['_updated_at'] = datetime.now()
        self.callback(mac_address, decoded_data)

