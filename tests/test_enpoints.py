from unittest import TestCase

import requests


class TestEndpoints(TestCase):

    def test_post_pool(self):
        file_bytes = '''
        http://localhost:8000        
        '''.encode()
        url = 'http://localhost:8282/proxies/testpool'
        values = {
            'file': ('test.txt', file_bytes),
        }
        resp = requests.post(url, files=values)
        print(resp.text)

    def test_patch_proxies(self):
        url = 'http://localhost:8282/proxies'
        values = {
            'parsed': 'test_parsed.txt',
        }
        resp_value = requests.patch(url, json=values)
        print(resp_value.text)

    def test_post_proxies(self):
        url = 'http://localhost:8282/proxies'
        post_values = {
            "parsed": "parsed.txt",
            "west": "west.txt",
        }
        value = requests.post(url, json=post_values)
        print(value.text)
