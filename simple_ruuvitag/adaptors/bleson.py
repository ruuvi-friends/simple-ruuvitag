import time
import logging
from bleson import get_provider, Observer

log = logging.getLogger(__name__)

class BlesonClient(object):
    '''Bluetooth LE communication with Bleson'''

    def __init__(self):
        self.observer = None

    def start(self, callback, bt_device=''):
        '''
        Attributes:
           callback: Function that recieves the data from BLE
           device (string): BLE device (default 0)
        '''

        if not bt_device:
            bt_device = 0
        else:
            # Old communication used hci0 etc.
            bt_device = bt_device.replace('hci', '')

        log.info('Observing broadcasts (device %s)', bt_device)

        adapter = get_provider().get_adapter(int(bt_device))
        self.observer = Observer(adapter)
        self.observer.on_advertising_data = callback
        self.observer.start()

        return self.observer

    def stop(self):
        self.observer.stop()
