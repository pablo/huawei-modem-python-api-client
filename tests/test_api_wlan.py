#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import faker
from mock import patch

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


if __name__ == '__main__':
    unittest.main()
