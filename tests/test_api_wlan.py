#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import faker
from mock import patch

import random
import six
import huaweisms.api.wlan
import huaweisms.api.common


class WlanTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fake = faker.Factory.create()

    @patch('huaweisms.api.common.get_from_url')
    def test_get_connected_hosts(self, mock_get_from_url):
        ctx = huaweisms.api.common.ApiCtx()
        huaweisms.api.wlan.get_connected_hosts(ctx)
        mock_get_from_url.assert_called_once_with(
            'http://192.168.8.1/api/wlan/host-list',
            ctx
        )

    @patch('huaweisms.api.common.get_from_url')
    def test_get_blocked_hosts(self, mock_get_from_url):
        fake_ip = self.fake.ipv4()
        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)
        huaweisms.api.wlan.get_blocked_hosts(ctx)
        mock_get_from_url.assert_called_once_with(
            'http://{}/api/wlan/multi-macfilter-settings'.format(fake_ip),
            ctx
        )

    @patch('huaweisms.api.wlan.get_blocked_hosts')
    def test_is_host_blocked_error_part_1(self, mock_get_blocked_hosts):
        fake_ip = self.fake.ipv4()
        fake_mac = self.fake.mac_address()

        mock_get_blocked_hosts.return_value = None
        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)

        with self.assertRaises(ValueError):
            huaweisms.api.wlan.is_host_blocked(ctx, fake_mac)
        mock_get_blocked_hosts.assert_called_once_with(ctx)

    @patch('huaweisms.api.wlan.get_blocked_hosts')
    def test_is_host_blocked_error_part_2(self, mock_get_blocked_hosts):
        fake_ip = self.fake.ipv4()
        fake_mac = self.fake.mac_address()

        mock_get_blocked_hosts.return_value = {"type": "bla"}
        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)

        with self.assertRaises(ValueError):
            huaweisms.api.wlan.is_host_blocked(ctx, fake_mac)
        mock_get_blocked_hosts.assert_called_once_with(ctx)

    @patch('huaweisms.api.wlan.get_blocked_hosts')
    def test_is_host_blocked__blocked_host(self, mock_get_blocked_hosts):
        fake_ip = self.fake.ipv4()
        fake_mac = self.fake.mac_address()

        mock_get_blocked_hosts.return_value = {
            "type": "response",
            "response": {
                "Ssids": {
                    "Ssid": [
                        {
                            "WifiMacFilterMac0": self.fake.mac_address(),
                            "WifiMacFilterMac1": self.fake.mac_address(),
                            "WifiMacFilterMac2": fake_mac,
                        }
                    ]
                }
            }
        }
        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)

        is_blocked = huaweisms.api.wlan.is_host_blocked(ctx, fake_mac)
        mock_get_blocked_hosts.assert_called_once_with(ctx)
        self.assertTrue(is_blocked)

    @patch('huaweisms.api.wlan.get_blocked_hosts')
    def test_is_host_blocked__unblocked_host(self, mock_get_blocked_hosts):
        fake_ip = self.fake.ipv4()
        fake_mac = self.fake.mac_address()

        mock_get_blocked_hosts.return_value = {
            "type": "response",
            "response": {
                "Ssids": {
                    "Ssid": [
                        {
                            "WifiMacFilterMac0": self.fake.mac_address(),
                            "WifiMacFilterMac1": self.fake.mac_address(),
                            "WifiMacFilterMac2": self.fake.mac_address(),
                        }
                    ]
                }
            }
        }
        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)

        is_blocked = huaweisms.api.wlan.is_host_blocked(ctx, fake_mac)
        mock_get_blocked_hosts.assert_called_once_with(ctx)
        self.assertFalse(is_blocked)

    @patch('huaweisms.api.wlan.is_host_blocked')
    @patch('huaweisms.api.wlan.get_blocked_hosts')
    @patch('huaweisms.xml.util.dict_to_xml')
    @patch('huaweisms.api.common.post_to_url')
    def test_block_host__already_blocked(self, mock_post_to_url, mock_dict_to_xml, mock_get_blocked_hosts,
                                         mock_is_host_blocked):
        mock_is_host_blocked.return_value = True
        fake_ip = self.fake.ipv4()
        fake_mac = self.fake.mac_address()
        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)
        result = huaweisms.api.wlan.block_host(ctx, fake_mac)
        self.assertTrue(result)
        mock_post_to_url.assert_not_called()
        mock_dict_to_xml.assert_not_called()
        mock_get_blocked_hosts.assert_not_called()
        mock_is_host_blocked.asset_called_once_with(ctx, fake_mac)

    @patch('huaweisms.api.wlan.is_host_blocked')
    @patch('huaweisms.api.wlan.get_blocked_hosts')
    @patch('huaweisms.xml.util.dict_to_xml')
    @patch('huaweisms.api.common.post_to_url')
    def test_block_host__slots_full(self, mock_post_to_url, mock_dict_to_xml,
                                    mock_get_blocked_hosts, mock_is_host_blocked):
        mock_is_host_blocked.return_value = False
        mock_get_blocked_hosts.return_value = {
            'type': 'response',
            'response': {
                "Ssids": {
                    "Ssid": [
                        {
                            'wifihostname{}'.format(i): '',
                            "WifiMacFilterMac{0}".format(i): self.fake.mac_address()
                        }
                        for i in range(10)
                    ]
                }
            }
        }
        fake_ip = self.fake.ipv4()
        fake_mac = self.fake.mac_address()
        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)

        error_msg = r'Failed to blacklist \[{}\], slots are full.'.format(fake_mac)
        with six.assertRaisesRegex(self, ValueError, error_msg):
            huaweisms.api.wlan.block_host(ctx, fake_mac)
        mock_post_to_url.assert_not_called()
        mock_dict_to_xml.assert_not_called()
        mock_get_blocked_hosts.assert_called_once_with(ctx)
        mock_is_host_blocked.asset_called_once_with(ctx, fake_mac)

    @patch('huaweisms.api.wlan.is_host_blocked')
    @patch('huaweisms.api.wlan.get_blocked_hosts')
    @patch('huaweisms.xml.util.dict_to_xml')
    @patch('huaweisms.api.common.post_to_url')
    def test_block_host__not_blocked(self, mock_post_to_url, mock_dict_to_xml,
                                     mock_get_blocked_hosts, mock_is_host_blocked):
        mock_is_host_blocked.return_value = False
        ret_val = {
            'type': 'response',
            'response': {
                "Ssids": {
                    "Ssid": [
                        {
                            'wifihostname{}'.format(i): '',
                            "WifiMacFilterMac{}".format(i): self.fake.mac_address()
                        }
                        for i in range(10)
                    ]
                }
            }
        }
        index = random.randint(0, 9)
        ret_val['response']['Ssids']['Ssid'][index] = {
            'wifihostname{}'.format(index): '',
            'WifiMacFilterMac{}'.format(index): ''
        }

        mock_get_blocked_hosts.return_value = ret_val
        mock_dict_to_xml.return_value = '<a>a</a>'

        fake_ip = self.fake.ipv4()
        fake_mac = self.fake.mac_address()
        fake_token = self.fake.sha256()

        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)
        ctx.tokens.append(fake_token)

        huaweisms.api.wlan.block_host(ctx, fake_mac)

        mock_post_to_url.assert_called_once_with(
            'http://{}/api/wlan/multi-macfilter-settings'.format(fake_ip),
            '<a>a</a>',
            ctx,
            additional_headers={'__RequestVerificationToken': fake_token}
        )
        mock_dict_to_xml.asset_called_once_with({'request': ret_val})
        mock_get_blocked_hosts.assert_called_once_with(ctx)
        mock_is_host_blocked.asset_called_once_with(ctx, fake_mac)

    @patch('huaweisms.api.wlan.is_host_blocked')
    @patch('huaweisms.api.wlan.get_blocked_hosts')
    @patch('huaweisms.xml.util.dict_to_xml')
    @patch('huaweisms.api.common.post_to_url')
    def test_unblock_host__not_blocked(self, mock_post_to_url, mock_dict_to_xml,
                                       mock_get_blocked_hosts, mock_is_host_blocked):
        mock_is_host_blocked.return_value = False

        fake_ip = self.fake.ipv4()
        fake_mac = self.fake.mac_address()
        fake_token = self.fake.sha256()

        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)
        ctx.tokens.append(fake_token)
        result = huaweisms.api.wlan.unblock_host(ctx, fake_mac)
        self.assertTrue(result is True)
        mock_is_host_blocked.assert_called_once_with(ctx, fake_mac)
        mock_post_to_url.assert_not_called()
        mock_dict_to_xml.assert_not_called()
        mock_get_blocked_hosts.assert_not_called()

    @patch('huaweisms.api.wlan.is_host_blocked')
    @patch('huaweisms.api.wlan.get_blocked_hosts')
    @patch('huaweisms.xml.util.dict_to_xml')
    @patch('huaweisms.api.common.post_to_url')
    def test_unblock_host__blocked(self, mock_post_to_url, mock_dict_to_xml,
                                   mock_get_blocked_hosts, mock_is_host_blocked):
        mock_is_host_blocked.return_value = True
        fake_mac = self.fake.mac_address()
        slots = {
            'type': 'response',
            'response': {
                "Ssids": {
                    "Ssid": [
                        {'wifihostname0': '', "WifiMacFilterMac0": self.fake.mac_address()},
                        {'wifihostname1': 'kajshdksj', 'WifiMacFilterMac1': fake_mac}
                    ]
                }
            }
        }
        mock_dict_to_xml.return_value = '<a>a</a>'
        mock_get_blocked_hosts.return_value = slots
        fake_ip = self.fake.ipv4()
        fake_token = self.fake.sha256()

        ctx = huaweisms.api.common.ApiCtx(modem_host=fake_ip)
        ctx.tokens.append(fake_token)
        huaweisms.api.wlan.unblock_host(ctx, fake_mac)

        mock_is_host_blocked.assert_called_once_with(ctx, fake_mac)
        mock_get_blocked_hosts.assert_called_once_with(ctx)
        print(slots)
        mock_dict_to_xml.assert_called_once_with({'request': slots['response']})
        mock_post_to_url.assert_called_once_with(
            'http://{}/api/wlan/multi-macfilter-settings'.format(fake_ip),
            '<a>a</a>',
            ctx,
            additional_headers={'__RequestVerificationToken': fake_token}
        )
        self.assertEqual(slots['response']['Ssids']['Ssid'][1]['wifihostname1'], '')
        self.assertEqual(slots['response']['Ssids']['Ssid'][1]['WifiMacFilterMac1'], '')


if __name__ == '__main__':
    unittest.main()
