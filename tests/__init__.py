import unittest
import requests

class TestFoo(unittest.TestCase):
    def test_is_up(self):
        # how should this work? 
        # discord fetches a specific URL
        # it should return the correspondingly-formatted html
        # self.assertIn()
        assert requests.get("https://psky.app/").status_code == 200
        assert requests.get("https://staging.psky.app/").status_code == 200

    def test_returns_correct_html(self):
        requests.get("")
        pass