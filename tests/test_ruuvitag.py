from unittest import TestCase
from mock import patch

from simple_ruuvitag.ruuvi import RuuviTagClient

# pylint: disable=line-too-long,no-self-use,unused-argument


class TestRuuviTag(TestCase):

    def mock_callbacks(self, callback):
        datas = [
            ('AA:2C:6A:1E:59:3D', '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD'),
            ('BB:2C:6A:1E:59:3D', 'some other device'),
            ('CC:2C:6A:1E:59:3D', '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD'),
            ('DD:2C:6A:1E:59:3D', '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD'),
            ('EE:2C:6A:1E:59:3D', '1F0201060303AAFE1716AAFE10F9037275752E76692F23416A5558314D417730C3'),
            ('FF:2C:6A:1E:59:3D', '1902010415FF990403291A1ECE1E02DEF94202CA0B5300000000BB'),
            ('00:2C:6A:1E:59:3D', '1902010415FF990403291A1ECE1E02DEF94202CA0B53BB'),
            ('11:2C:6A:1E:59:3D', '043E2B020100014F884C33B8CB1F0201061BFF99040512FC5394C37C0004FFFC040CAC364200CDCBB8334C884FC4')
        ]

        for data in datas:
            callback(data)

    @patch('simple_ruuvitag.adaptors.dummy.DummyBle.mock_datas', mock_callbacks)
    def test_get_current_datas(self):
        macs = ['CC:2C:6A:1E:59:3D', 'DD:2C:6A:1E:59:3D', 'EE:2C:6A:1E:59:3D']

        ble_client = RuuviTagClient(adapter='dummy')
        ble_client.listen(mac_addresses=macs)

        data = ble_client.get_current_datas()

        self.assertEqual(3, len(data))
        self.assertTrue('CC:2C:6A:1E:59:3D' in data)
        self.assertTrue('DD:2C:6A:1E:59:3D' in data)
        self.assertTrue(data['CC:2C:6A:1E:59:3D']['temperature'] == 24.0)
        self.assertTrue(data['EE:2C:6A:1E:59:3D']['temperature'] == 25.12)
        self.assertTrue(data['EE:2C:6A:1E:59:3D']['identifier'] == '0')

        data = ble_client.get_current_datas(consume=True)


    @patch('simple_ruuvitag.adaptors.dummy.DummyBle.mock_datas', mock_callbacks)
    def test_get_current_datas_without_filters(self):
        macs = None

        ble_client = RuuviTagClient(adapter='dummy')
        ble_client.listen(mac_addresses=macs)

        data = ble_client.get_current_datas()

        self.assertEqual(7, len(data))

    @patch('simple_ruuvitag.adaptors.dummy.DummyBle.mock_datas', mock_callbacks)
    def test_get_current_datas_with_consume(self):

        ble_client = RuuviTagClient(adapter='dummy')
        ble_client.listen()

        ble_client.get_current_datas(consume=True)
        mew_data = ble_client.get_current_datas(consume=True)
        self.assertEqual(0, len(mew_data))

    @patch('simple_ruuvitag.adaptors.dummy.DummyBle.mock_datas', mock_callbacks)
    def test_blackisting_of_other_macs(self):

        ble_client = RuuviTagClient(adapter='dummy')
        ble_client.listen()

        self.assertTrue('BB:2C:6A:1E:59:3D' in ble_client.mac_blacklist)
