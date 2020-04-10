
class BluetoothAdaptor(object):

    def __init__(self, callback, bt_device=''):
        '''
        Arguments:
           callback: Function that receives the data from BLE
           device (string): BLE device (default 0)
        '''

        self.callback = callback
