

class DummyBle(object):
    '''Bluetooth LE communication with Bleson'''

    def mock_datas(self, callback):
        
        callback(('DU:MM:YD:AT:A9:3D',
             '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD'))
        
        callback(('NO:TS:UP:PO:RT:ED',
             '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD'))

    def __init__(self):
        self.observer = None

    def start(self, callback, bt_device=''):

        # Simulates the call to the callback
        self.mock_datas(callback)

        return None

    def stop(self):
        pass