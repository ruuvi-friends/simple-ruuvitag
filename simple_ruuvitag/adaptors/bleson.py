import logging
from logging import INFO, DEBUG, WARN, WARNING, ERROR
from simple_ruuvitag.adaptors import BluetoothAdaptor
from bleson import get_provider, Observer, set_level

log = logging.getLogger(__name__)
# set_level(DEBUG)

class BlesonClient(BluetoothAdaptor):
    '''Bluetooth LE communication with Bleson'''

    def handle_callback(self, advertisement):
        if not advertisement.mfg_data:
            return

        processed_data = {
            # WARNING, Apple sucks, so it does not provide mac address
            # in the advertisement! Go tell them that they suck!
            # https://forums.developer.apple.com/thread/8442
            "address": advertisement.address if advertisement.address else None,
            "raw_data": advertisement.raw_data.hex(),
            "tx_power": advertisement.tx_power,
            "rssi": advertisement.rssi,
            "name": advertisement.name,
        }

        if processed_data["raw_data"][0:2] != 'FF':
            processed_data["raw_data"] = 'FF' + processed_data["raw_data"]

        self.callback(processed_data)

    def __init__(self, callback, bt_device=''):
        '''
        Arguments:
           callback: Function that receives the data from BLE
           device (string): BLE device (default 0)
        '''
        super().__init__(callback, bt_device)

        self.observer = None

        if not bt_device:
            bt_device = 0
        else:
            # Old communication used hci0 etc.
            bt_device = bt_device.replace('hci', '')

        log.info('Observing broadcasts (device %s)', bt_device)

        adapter = get_provider().get_adapter(int(bt_device))
        self.observer = Observer(adapter)
        self.observer.on_advertising_data = self.handle_callback

    def start(self):
        if not self.observer:
            log.info('Cannot start a client that has not been setup')
            return
        self.observer.start()

    def stop(self):
        self.observer.stop()
