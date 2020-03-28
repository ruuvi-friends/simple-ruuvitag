import time
import logging
from bleson import get_provider, Observer

log = logging.getLogger(__name__)

class BlesonClient(object):
    '''Bluetooth LE communication with Bleson'''

    def __init__(self):
        self.observer = None
        self.callback = None


    def handle_callback(self, advertisment):
        
        if not advertisment.mfg_data:
            # No data to return
            return
        
        processed_data = {
            "address": advertisment.address.address,
            "raw_data": "FF" + advertisment.mfg_data.hex(),
            # these are documented but don't work
            # "tx_power": data.tx_power,
            # "rssi": data.rssi,
            # "name": data.name,
        }
        self.callback(processed_data)

    def start(self):
        if not self.observer:
            log.info('Cannot start a client that has not been setup')
            return
        self.observer.start()

    def setup(self, callback, bt_device=''):
        '''
        Attributes:
           callback: Function that recieves the data from BLE
           device (string): BLE device (default 0)
        '''

        # set callback
        self.callback = callback

        if not bt_device:
            bt_device = 0
        else:
            # Old communication used hci0 etc.
            bt_device = bt_device.replace('hci', '')

        log.info('Observing broadcasts (device %s)', bt_device)

        adapter = get_provider().get_adapter(int(bt_device))
        self.observer = Observer(adapter)
        self.observer.on_advertising_data = self.handle_callback

        return self.observer

    def stop(self):
        self.observer.stop()
