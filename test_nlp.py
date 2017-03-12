# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from fetching_booking_api import get_nlp_result


class TaipeiHacksNLPTestCase(unittest.TestCase):

    def test_nlp_up(self):
        result = get_nlp_result("up")
        self.assertIsNone(result)

    def test_nlp_down(self):
        result = get_nlp_result("down")
        self.assertIsNone(result)

    def test_nlp_lexus(self):
        result = get_nlp_result("lexus")
        self.assertIsNone(result)

    def test_nlp_price_up(self):
        result = get_nlp_result("price up")
        self.assertEqual(("price", "up"), result)

    def test_nlp_rich(self):
        result = get_nlp_result("rich")
        self.assertEqual(("all", "up"), result)

    def test_nlp_luxury(self):
        result = get_nlp_result("give me luxury")
        self.assertEqual(("all", "up"), result)

    def test_nlp_cheaper(self):
        result = get_nlp_result("cheaper")
        self.assertEqual(("price", "down"), result)

if __name__ == '__main__':
    unittest.main()
