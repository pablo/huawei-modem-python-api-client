#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest


import huaweisms.api.common


class ApiCommonTestCase(unittest.TestCase):

    def test_common_headers(self):
        expected = {"X-Requested-With": "XMLHttpRequest"}
        data = huaweisms.api.common.common_headers()
        self.assertDictEqual(data, expected)


if __name__ == '__main__':
    unittest.main()
