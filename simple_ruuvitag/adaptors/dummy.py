import logging
from simple_ruuvitag.adaptors import BluetoothAdaptor

log = logging.getLogger(__name__)

class DummyBle(BluetoothAdaptor):
    '''Bluetooth LE communication with Bleson'''

    def mock_datas(self, callback):

        callback(
            {
                "address": 'DU:MM:YD:AT:A9:3D',
                "raw_data": '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD',
                "tx_power": 0,
                "rssi": -99,
                "name": 'bleson',
            }
        )

        callback(
            {
                "address": 'NO:TS:UP:PO:RT:ED',
                "raw_data": '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD',
                "tx_power": 0,
                "rssi": -99,
                "name": 'bleson',
            }
        )

    def start(self):

        # Simulates the call to the callback
        self.mock_datas(self.callback)

        return None

    def stop(self):
        # dummy BLE cannot stop.
        pass
