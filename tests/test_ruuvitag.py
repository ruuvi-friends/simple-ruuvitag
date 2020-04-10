from unittest import TestCase
from mock import patch

from simple_ruuvitag.ruuvi import RuuviTagClient

# pylint: disable=line-too-long,no-self-use,unused-argument


class TestRuuviTag(TestCase):

    def mock_callbacks(self, callback):
        datas = [
            {
                "address": 'AA:2C:6A:1E:59:3D',
                "raw_data": '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD',
            },
            {
                "address": 'BB:2C:6A:1E:59:3D',
                "raw_data": 'some other device',
            },
            {
                "address": 'CC:2C:6A:1E:59:3D',
                "raw_data": '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD',
            },
            {
                "address": 'DD:2C:6A:1E:59:3D',
                "raw_data": '1E0201060303AAFE1616AAFE10EE037275752E76692F23416A7759414D4663CD',
            },
            {
                "address": 'EE:2C:6A:1E:59:3D',
                "raw_data": '1F0201060303AAFE1716AAFE10F9037275752E76692F23416A5558314D417730C3',
            },
            {
                "address": 'FF:2C:6A:1E:59:3D',
                "raw_data": '1902010415FF990403291A1ECE1E02DEF94202CA0B5300000000BB',
            },
            {
                "address": '00:2C:6A:1E:59:3D',
                "raw_data": '1902010415FF990403291A1ECE1E02DEF94202CA0B53BB',
            },
            {
                "address": '11:2C:6A:1E:59:3D',
                "raw_data": '043E2B020100014F884C33B8CB1F0201061BFF99040512FC5394C37C0004FFFC040CAC364200CDCBB8334C884FC4'
            },
            # In version data format 5 mac is in payload. Mac os does not return mac on BLE advertisment 
            # so we need to support that usecase of getting the mac address from the payload
            {
                "address": None,
                "raw_data": '043E2B020100014F884C33B8CB1F0201061BFF99040512FC5394C37C0004FFFC040CAC364200CDCBB8334C884FC4'
            },
            # This one is thrown away because we don't have the mac, and mac is not in payload
            {
                "address": None,
                "raw_data": '1902010415FF990403291A1ECE1E02DEF94202CA0B53BB',
            },
        ]

        for data in datas:
            callback(data)

    @patch('simple_ruuvitag.adaptors.dummy.DummyBle.mock_datas', mock_callbacks)
    def test_get_current_datas(self):
        macs = ['CC:2C:6A:1E:59:3D', 'DD:2C:6A:1E:59:3D', 'EE:2C:6A:1E:59:3D']

        ble_client = RuuviTagClient(mac_addresses=macs, adapter='dummy')
        ble_client.start()

        data = ble_client.get_current_datas()

        self.assertEqual(4, len(data))
        self.assertTrue('CC:2C:6A:1E:59:3D' in data)
        self.assertTrue('DD:2C:6A:1E:59:3D' in data)
        self.assertTrue(data['CC:2C:6A:1E:59:3D']['temperature'] == 24.0)
        self.assertTrue(data['EE:2C:6A:1E:59:3D']['temperature'] == 25.12)
        self.assertTrue(data['EE:2C:6A:1E:59:3D']['identifier'] == '0')

        data = ble_client.get_current_datas(consume=True)


    @patch('simple_ruuvitag.adaptors.dummy.DummyBle.mock_datas', mock_callbacks)
    def test_get_current_datas_without_filters(self):
        macs = None

        ble_client = RuuviTagClient(mac_addresses=macs, adapter='dummy')
        ble_client.start()

        data = ble_client.get_current_datas()

        self.assertEqual(8, len(data))

    @patch('simple_ruuvitag.adaptors.dummy.DummyBle.mock_datas', mock_callbacks)
    def test_get_current_datas_with_consume(self):

        ble_client = RuuviTagClient(adapter='dummy')
        ble_client.start()

        ble_client.get_current_datas(consume=True)
        mew_data = ble_client.get_current_datas(consume=True)
        self.assertEqual(0, len(mew_data))

    @patch('simple_ruuvitag.adaptors.dummy.DummyBle.mock_datas', mock_callbacks)
    def test_blackisting_of_other_macs(self):

        ble_client = RuuviTagClient(adapter='dummy')
        ble_client.start()

        self.assertTrue('BB:2C:6A:1E:59:3D' in ble_client.mac_blacklist)
