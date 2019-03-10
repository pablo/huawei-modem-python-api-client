#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import faker

import huaweisms.api.common


class ApiCommonTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fake = faker.Factory.create()

    def test_common_headers(self):
        expected = {"X-Requested-With": "XMLHttpRequest"}
        data = huaweisms.api.common.common_headers()
        self.assertDictEqual(data, expected)

    def test_build_cookies(self):
        ctx = huaweisms.api.common.ApiCtx()
        cookies = huaweisms.api.common.build_cookies(ctx)
        self.assertIsNone(cookies)

        fake_id = self.fake.sha256()
        ctx.session_id = fake_id
        cookies = huaweisms.api.common.build_cookies(ctx)
        self.assertIsInstance(cookies, dict)
        self.assertDictEqual(cookies, {'SessionID': fake_id})


if __name__ == '__main__':
    unittest.main()
