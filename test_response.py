# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import taipeihacks


class TaipeiHacksTestCase(unittest.TestCase):
    def setUp(self):
        self.app = taipeihacks.app.test_client()

    def test_welcome(self):
        url = ('/api/v1/welcome?fb_id=58c35c25e4b017a29d04b7fb&'
               'ref=2017-06-01%2C2017-06-02%2CTokyo&price=100&review_scores=7&stars=3')
        result = self.app.get(url)
        self.assertEqual(200, result.status_code)

    def test_choose(self):
        url = ("/api/v1/choose?user_text=cheaper&fb_id=58c35c25e4b017a29d04b7fb&"
               "ref=2017-06-01%2C2017-06-02%2CTokyoTower&price=100&review_scores=7&stars=3")
        result = self.app.get(url)
        self.assertEqual(200, result.status_code)


if __name__ == '__main__':
    unittest.main()
