from unittest import TestCase

import requests


class TestEndpoints(TestCase):
    def test_get_pool(self):
        url = 'http://localhost:8182/proxies/parsed?method=pool'
        resp_value = requests.get(url).text
        self.assertTrue('http' in resp_value)
